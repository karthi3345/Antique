#!/usr/bin/env python3
"""Refetch pass 2: replace off-target objects with proper museum objects.

Removes bad records + their image dirs, then continues fetching with
tightened queries and stricter filtering until each category has exactly
8 well-matched public-domain objects.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from io import BytesIO

from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from fetch_museum_images import (  # noqa: E402
    API, OUT_ROOT, DATA_DIR, JSON_PATH, PER_CATEGORY, UA,
    http_json, http_bytes, normalize_to_stage,
)

# Records whose titles make clear they are not the right kind of object.
TITLE_BLOCKLIST = [
    "the harvesters", "view of toledo", "damascus room", "spartan soldier",
    "fan mount", "polyptych", "dancers", "desk (secretary)", "desk",
    "painting", "photograph", "drawing", "print", "study for", "design for",
    "model of", "fragment of a", "box for", "case for", "cover for",
]

# department must be one of these object departments
GOOD_DEPARTMENTS = {
    "European Sculpture and Decorative Arts",
    "The Cloisters",
    "Arms and Armor",
    "Musical Instruments",
    "Ancient Near Eastern Art",
    "Egyptian Art",
    "Greek and Roman Art",
    "Asian Art",
    "Medieval Art",
    "Robert Lehman Collection",
    "Islamic Art",
}

# Tighter queries per category.
QUERIES = {
    "Furniture": [
        "cabinet ebony", "cabinet oak carved", "bureau plat", "fall-front desk",
        "armchair beechwood", "fauteuil", "commode kingwood", "chest walnut",
        "table walnut marble top", "wardrobe walnut",
    ],
    "Sculpture": [
        "bronze statuette", "marble bust", "terracotta statuette",
        "boxwood", "alabaster figure", "limestone virgin", "bronze figure",
        "wood polychrome sculpture",
    ],
    "Scientific Instruments": [
        "astrolabe", "brass telescope", "microscope", "sextant navigational",
        "sundial brass", "armillary sphere", "nocturnal", "quadrant brass",
        "theodolite", "clock balance spring",
    ],
    "Ceramics": [
        "porcelain vase", "delftware dish", "faience dish", "stoneware",
        "porcelain bowl blue", "tankard pewter", "ewer porcelain",
        "covered porcelain jar",
    ],
    "Arms & Armour": [
        "armor garniture", "breastplate", "close helmet", "sword rapier",
        "buckler", "halberd", "morion", "gauntlet", "sword hilted",
    ],
    "Metalwork": [
        "tankard silver", "ewer silver", "basin brass", "candlestick bronze",
        "censer bronze", "incense burner", "aquamanile", "beaker silver gilt",
        "cup silver", "plate brass engraved",
    ],
    "Glass": [
        "glass goblet venetian", "glass tazza", "spear glass façon",
        "flask glass mold-blown", "glass beaker enameled", "glass ewer",
        "cruet glass", "glass bowl ancient",
    ],
}

CATEGORY_MATCH = {
    # require the classification or title to match one of these substrings
    "Furniture": ("furniture",),
    "Sculpture": ("sculpture",),
    "Scientific Instruments": ("instruments", "horology"),
    "Ceramics": ("ceramics",),
    "Arms & Armour": ("arms and armor", "armor"),
    "Metalwork": ("metalwork", "metal"),
    "Glass": ("glass",),
}


def title_ok(t):
    tl = t.lower()
    return not any(b in tl for b in TITLE_BLOCKLIST)


def dept_ok(obj):
    dept = (obj.get("department") or "").strip()
    return dept in GOOD_DEPARTMENTS


def class_ok(obj, category):
    cl = (obj.get("classification") or "").strip().lower()
    keys = CATEGORY_MATCH[category]
    if not cl:
        return False
    return any(k in cl for k in keys)


def main():
    records = json.load(open(JSON_PATH))
    # Drop bad records and delete their dirs
    keep = []
    dropped = []
    for r in records:
        if not title_ok(r["name"]):
            dropped.append((r["object_number"], r["name"], r["category"]))
            d = os.path.join(OUT_ROOT, f"{r['object_number']:03d}")
            if os.path.isdir(d):
                for f in os.listdir(d):
                    os.remove(os.path.join(d, f))
                os.rmdir(d)
        else:
            keep.append(r)
    print(f"Dropped {len(dropped)}:")
    for d in dropped:
        print("  -", d)

    # Re-fetch to fill gaps
    counts = {}
    for r in keep:
        counts[r["category"]] = counts.get(r["category"], 0) + 1
    existing_met_ids = {r["met_object_id"] for r in keep}

    next_number = max(r["object_number"] for r in keep) + 1 if keep else 1

    for category, queries in QUERIES.items():
        got = counts.get(category, 0)
        if got >= PER_CATEGORY:
            continue
        print(f"\n=== {category} — have {got}")
        for term in queries:
            if got >= PER_CATEGORY:
                break
            try:
                res = http_json(f"{API}/search?q={urllib.parse.quote(term)}&hasImages=true")
            except Exception as e:
                print(f"  search '{term}' failed: {e}")
                continue
            ids = (res.get("objectIDs") or [])[:80]
            for oid in ids:
                if got >= PER_CATEGORY:
                    break
                if oid in existing_met_ids:
                    continue
                try:
                    obj = http_json(f"{API}/objects/{oid}")
                except Exception as e:
                    continue
                if not obj.get("isPublicDomain") or not obj.get("primaryImage"):
                    continue
                if not title_ok(obj.get("title", "")) or not dept_ok(obj) or not class_ok(obj, category):
                    continue
                try:
                    raw = http_bytes(obj["primaryImage"])
                except Exception:
                    continue
                stage = normalize_to_stage(raw)
                n = next_number
                out_dir = os.path.join(OUT_ROOT, f"{n:03d}")
                os.makedirs(out_dir, exist_ok=True)
                stage.save(os.path.join(out_dir, "00.webp"), "WEBP", quality=82, method=4)

                date = (obj.get("objectDate") or "").strip() or "Undated"
                nums = re.findall(r"(?<!\d)([1-9][0-9]{2,3})(?!\d)", date)
                ys = int(nums[-1]) if nums else 1500
                if "b.c" in date.lower():
                    ys = -abs(ys)
                region = (obj.get("culture") or obj.get("country") or obj.get("dynasty") or "").strip()
                if not region:
                    region = (obj.get("artistDisplayName") or "Unknown").strip()
                medium = (obj.get("medium") or "Mixed media").split(";")[0].split(".")[0].strip()
                record = {
                    "object_number": n,
                    "met_object_id": oid,
                    "name": obj["title"].strip(),
                    "period": date,
                    "period_sort": ys,
                    "region": region,
                    "category": category,
                    "material": medium or "Mixed media",
                    "dimensions": (obj.get("dimensions") or "").split(";")[0].strip(),
                    "maker": (obj.get("artistDisplayName") or "Unsigned").strip() or "Unsigned",
                    "image_source": "The Metropolitan Museum of Art",
                    "image_source_url": obj.get("objectURL", ""),
                    "image_license": "Open Access CC0",
                    "image_credit": obj.get("creditLine", ""),
                    "accession": obj.get("accessionNumber", ""),
                    "gallery": obj.get("GalleryNumber", "") or "",
                }
                keep.append(record)
                existing_met_ids.add(oid)
                counts[category] = got = got + 1
                next_number = n + 1
                print(f"  + No.{n:03d} [{category}] {record['name'][:55]} ({record['period']}) [{obj.get('classification','')}]")
                time.sleep(0.2)

    json.dump(keep, open(JSON_PATH, "w"), indent=2)
    print(f"\nTotal {len(keep)}")
    c = {}
    for r in keep:
        c[r["category"]] = c.get(r["category"], 0) + 1
    print(json.dumps(c, indent=2))


if __name__ == "__main__":
    main()
