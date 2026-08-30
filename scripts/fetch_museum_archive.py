#!/usr/bin/env python3
"""Canonical museum-archive fetcher for VOLGO (The Met Open Access, CC0).

Robust against the Met API's occasional 403 rate-limit bursts:
- every accepted object is saved to disk AND appended to the JSON immediately
- 403/5xx responses back off 60s and retry (max 5)
- polite 0.35s delay between metadata calls

Categories × 8 objects. Strict validation: CC0 only, object departments only,
classification must match the category, title blocklist, image required.

Run: python3 scripts/fetch_museum_archive.py
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from fetch_museum_images import (  # noqa: E402
    API, OUT_ROOT, DATA_DIR, JSON_PATH, UA,
    http_bytes, normalize_to_stage,
)

PER_CATEGORY = 8
CATEGORY_ORDER = [
    "Furniture", "Sculpture", "Scientific Instruments", "Ceramics",
    "Arms & Armour", "Metalwork", "Glass",
]

# search term → departmentIds filter for the Met /search endpoint
# dept 12 = European Sculpture and Decorative Arts, 4 = Arms and Armor,
# 14 = Islamic Art, 18 = Musical Instruments, 1 = American Decorative Arts,
# 13 = Greek and Roman Art, 17 = Medieval Art, 6 = Asian Art, 3 = Ancient Near East
SEARCHES = {
    "Furniture": [
        ("cabinet", "12"), ("commode", "12"), ("writing table", "12"),
        ("armchair", "12"), ("secretary desk", "12"), ("chest drawers walnut", "12"),
        ("bureau", "12"), ("table marble top", "12"), ("wardrobe", "12"),
    ],
    "Sculpture": [
        ("bronze statuette", "12"), ("marble bust", "12"),
        ("terracotta statuette", "12"), ("bronze figure", "12"),
        ("limestone figure", "12"), ("boxwood", "12"), ("biscuit porcelain figure", "12"),
        ("alabaster", "17"),
    ],
    "Scientific Instruments": [
        ("astrolabe", ""), ("sundial", "12"), ("armillary sphere", ""),
        ("telescope", ""), ("microscope", ""), ("sextant", ""),
        ("quadrant", "14"), ("clock", "12"), ("nocturnal", ""), ("theodolite", ""),
    ],
    "Ceramics": [
        ("porcelain vase", "12"), ("delftware", "12"), ("faience dish", "12"),
        ("stoneware jar", "12"), ("porcelain bowl", "12"), ("majolica", "12"),
        ("covered jar porcelain", "12"), ("teapot porcelain", "12"),
    ],
    "Arms & Armour": [
        ("armor", "4"), ("helmet", "4"), ("breastplate", "4"),
        ("sword", "4"), ("rapier", "4"), ("buckler", "4"), ("halberd", "4"),
        ("gauntlet", "4"), ("morion", "4"),
    ],
    "Metalwork": [
        ("silver tankard", "12"), ("silver ewer", "12"), ("candlestick", "12"),
        ("bronze aquamanile", "12"), ("censer", "14"), ("brass basin", "12"),
        ("silver cup", "12"), ("pewter", "12"), ("bronze incense", "14"),
    ],
    "Glass": [
        ("glass goblet", "12"), ("glass tazza", "12"), ("glass flask", "12"),
        ("glass beaker", "12"), ("venetian glass", "12"), ("glass ewer", "12"),
        ("façon de venise", "12"), ("glass bowl", "14"), ("cruet glass", "12"),
    ],
}

GOOD_DEPARTMENTS = {
    "European Sculpture and Decorative Arts", "The Cloisters",
    "Arms and Armor", "Musical Instruments", "Ancient Near Eastern Art",
    "Egyptian Art", "Greek and Roman Art", "Asian Art", "Medieval Art",
    "Robert Lehman Collection", "Islamic Art", "The American Wing",
}

TITLE_BLOCKLIST = [
    "the harvesters", "view of toledo", "damascus room", "spartan soldier",
    "fan mount", "polyptych", "dancers", "desk (secretary)",
    "painting", "photograph", "drawing", "print", "study for", "design for",
    "model of", "fragment", "box for", "case for", "cover for",
    "manuscript", "book", "textile", "embroidered", "tapestry",
]

# classification substrings that qualify per category (lowercase)
CLASS_MATCH = {
    "Furniture": ("furniture", "woodwork"),
    "Sculpture": ("sculpture",),
    "Scientific Instruments": ("scientific instruments", "clocks", "horology"),
    "Ceramics": ("ceramics", "porcelain", "pottery", "faience", "stoneware"),
    "Arms & Armour": (),  # department check is authoritative
    "Metalwork": ("metalwork", "metal", "silver", "gold", "pewter", "copper"),
    "Glass": ("glass",),
}


def http_json_robust(url, tries=5):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 500, 502, 503):
                wait = 60 * (attempt + 1)
                print(f"    [rate-limited {e.code}] backing off {wait}s…")
                time.sleep(wait)
                continue
            raise
        except Exception:
            if attempt == tries - 1:
                raise
            time.sleep(5)
    return None


def title_ok(t):
    tl = (t or "").lower()
    return bool(t) and len(t) >= 4 and not any(b in tl for b in TITLE_BLOCKLIST)


def valid_for(obj, category):
    if not obj.get("isPublicDomain") or not obj.get("primaryImage"):
        return False
    if not title_ok(obj.get("title", "")):
        return False
    if (obj.get("department") or "").strip() not in GOOD_DEPARTMENTS:
        return False
    cl = (obj.get("classification") or "").strip().lower()
    allowed = CLASS_MATCH[category]
    if allowed and not cl:
        return False
    if allowed and not any(k in cl for k in allowed):
        return False
    return True


def make_record(obj, category, n):
    date = (obj.get("objectDate") or "").strip() or "Undated"
    ys = obj.get("objectBeginDate") or 1500
    try:
        ys = int(ys)
    except (TypeError, ValueError):
        ys = 1500
    region = " or ".join(
        v for v in (
            obj.get("country"), obj.get("culture"),
            obj.get("reign"), obj.get("artistNationality"),
        ) if (v or "").strip()
    ) or (obj.get("artistDisplayName") or "Unknown").strip() or "Unknown"
    medium = (obj.get("medium") or "Mixed media").split(";")[0].split(".")[0].strip()
    return {
        "object_number": n,
        "met_object_id": obj["objectID"],
        "name": obj["title"].strip(),
        "period": date,
        "period_sort": ys,
        "region": region,
        "category": category,
        "material": medium or "Mixed media",
        "dimensions": (obj.get("dimensions") or "").split(";")[0].strip(),
        "maker": (obj.get("artistDisplayName") or "Unsigned").strip() or "Unsigned",
        "object_name": (obj.get("objectName") or "").strip(),
        "image_source": "The Metropolitan Museum of Art",
        "image_source_url": obj.get("objectURL", ""),
        "image_license": "Open Access CC0",
        "image_credit": obj.get("creditLine", ""),
        "accession": obj.get("accessionNumber", ""),
        "gallery": obj.get("GalleryNumber", "") or "",
    }


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUT_ROOT, exist_ok=True)

    # load incremental state
    records = []
    if os.path.exists(JSON_PATH):
        records = json.load(open(JSON_PATH))
    existing_ids = {r["met_object_id"] for r in records}
    next_number = max((r["object_number"] for r in records), default=0) + 1

    def persist():
        json.dump(records, open(JSON_PATH, "w"), indent=2)

    for category in CATEGORY_ORDER:
        got = sum(1 for r in records if r["category"] == category)
        print(f"\n=== {category}: have {got}")
        if got >= PER_CATEGORY:
            continue
        for term, dept in SEARCHES[category]:
            if got >= PER_CATEGORY:
                break
            q = f"{API}/search?q={urllib.parse.quote(term)}&hasImages=true"
            if dept:
                q += f"&departmentIds={dept}"
            try:
                res = http_json_robust(q)
            except Exception as e:
                print(f"  search '{term}' failed: {e}")
                continue
            ids = (res or {}).get("objectIDs") or []
            # interleave so we skim highlights first if present
            for oid in ids[:140]:
                if got >= PER_CATEGORY:
                    break
                if oid in existing_ids:
                    continue
                try:
                    obj = http_json_robust(f"{API}/objects/{oid}")
                except Exception as e:
                    print(f"    obj {oid} failed: {e}")
                    continue
                if not obj or not valid_for(obj, category):
                    time.sleep(0.12)
                    continue
                try:
                    raw = http_bytes(obj["primaryImage"])
                except Exception as e:
                    print(f"    img {oid} failed: {e}")
                    continue
                stage = normalize_to_stage(raw)
                n = next_number
                out_dir = os.path.join(OUT_ROOT, f"{n:03d}")
                os.makedirs(out_dir, exist_ok=True)
                stage.save(os.path.join(out_dir, "00.webp"), "WEBP", quality=82, method=4)
                rec = make_record(obj, category, n)
                records.append(rec)
                existing_ids.add(oid)
                persist()  # incremental save
                next_number = n + 1
                got += 1
                print(f"    + No.{n:03d} [{category}] {rec['name'][:52]} ({rec['period'][:24]})")
                time.sleep(0.35)

    persist()
    counts = {}
    for r in records:
        counts[r["category"]] = counts.get(r["category"], 0) + 1
    print("\nDone:", json.dumps(counts, indent=2), "total", len(records))


if __name__ == "__main__":
    main()
