#!/usr/bin/env python3
"""Fetch 56 real museum objects (8 per category) from The Met Open Access API.

- Only IsPublicDomain=true objects are accepted (CC0).
- Downloads the original primaryImage, normalizes to a warm-ivory stage,
  center-crops to 4:5, converts to WebP (long edge 1400px) at
  static/img/objects/NNN/00.webp.
- Writes collection/data/museum_objects.json with full provenance metadata
  (source, source_url, license, credit) used by the seeder.

Run:  python3 scripts/fetch_museum_images.py
Idempotent: skips objects whose images already exist on disk.
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error
from io import BytesIO

from PIL import Image

API = "https://collectionapi.metmuseum.org/public/collection/v1"
OUT_ROOT = os.path.join(os.path.dirname(__file__), "..", "static", "img", "objects")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "collection", "data")
JSON_PATH = os.path.join(DATA_DIR, "museum_objects.json")

# Per category: a curated list of (search term, max objects) queries. We walk
# the queries in order until we have PER_CATEGORY accepted objects.
CATEGORY_QUERIES = {
    "Furniture": [
        ("cabinet marquetry", 10),
        ("writing table", 10),
        ("armchair walnut", 10),
        ("commode", 10),
        ("chest of drawers", 10),
        ("sideboard", 10),
    ],
    "Sculpture": [
        ("bronze statuette", 10),
        ("marble bust portrait", 10),
        ("ivory sculpture", 10),
        ("terracotta figure", 10),
        ("wood sculpture virgin", 10),
    ],
    "Scientific Instruments": [
        ("astrolabe", 10),
        ("telescope", 10),
        ("microscope brass", 10),
        ("sextant", 10),
        ("sundial", 10),
        ("armillary sphere", 10),
        ("barometer", 10),
        ("compass", 10),
    ],
    "Ceramics": [
        ("porcelain vase", 10),
        ("delftware", 10),
        ("majolica dish", 10),
        ("stoneware jar", 10),
        ("porcelain bowl", 10),
        ("faience", 10),
    ],
    "Arms & Armour": [
        ("armor Greenwich", 10),
        ("helm", 10),
        ("sword rapier", 10),
        ("buckler shield", 10),
        ("halberd", 10),
        ("morion", 10),
    ],
    "Metalwork": [
        ("silver tankard", 10),
        ("bronze vessel", 10),
        ("candlestick brass", 10),
        ("silver ewer", 10),
        ("censer", 10),
        ("incense burner bronze", 10),
    ],
    "Glass": [
        ("venetian glass goblet", 10),
        ("glass vessel ancient", 10),
        ("enameled glass", 10),
        ("glass flask", 10),
        ("facon de venise", 10),
        ("glass beaker", 10),
    ],
}

PER_CATEGORY = 8
IVORY = (241, 235, 221)  # matches --ivory token
STAGE_W, STAGE_H = 1120, 1400  # 4:5
TARGET_LONG_EDGE = 1400

UA = {"User-Agent": "VolgoArchive/1.0 (research; contact: curator@volgo.example)"}


def http_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def http_bytes(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def normalize_to_stage(jpg_bytes):
    """Place the museum photo on a warm-ivory 4:5 stage, undistorted."""
    im = Image.open(BytesIO(jpg_bytes)).convert("RGB")
    # Downscale first for speed if huge
    w, h = im.size
    scale = min(1.0, 1600.0 / max(w, h))
    if scale < 1.0:
        im = im.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    stage = Image.new("RGB", (STAGE_W, STAGE_H), IVORY)
    # Fit inside stage with 6% padding
    pad = 0.06
    avail_w, avail_h = int(STAGE_W * (1 - 2 * pad)), int(STAGE_H * (1 - 2 * pad))
    w, h = im.size
    s = min(avail_w / w, avail_h / h)
    im = im.resize((max(1, int(w * s)), max(1, int(h * s))), Image.LANCZOS)
    stage.paste(im, ((STAGE_W - im.width) // 2, (STAGE_H - im.height) // 2))
    # Long-edge cap (already 1400 on the short side; keep quality)
    if max(stage.size) > TARGET_LONG_EDGE + 400:
        stage.thumbnail((TARGET_LONG_EDGE, TARGET_LONG_EDGE), Image.LANCZOS)
    return stage


def acceptable(obj):
    if not obj.get("isPublicDomain"):
        return False, "not public domain"
    if not obj.get("primaryImage"):
        return False, "no primary image"
    title = obj.get("title", "")
    if not title or len(title) < 4:
        return False, "no title"
    date = obj.get("objectDate", "")
    if not date or date.lower().startswith("19") and date[:2] == "19" and "century" not in date.lower():
        pass  # keep — Met dates are fine as-is
    # Skip photographs/drawings/paintings — we want objects
    bad = obj.get("classification", "") or ""
    for skip in ("Photograph", "Painting", "Drawing", "Print", "Textile",
                 "Book", "Manuscript", "Codices"):
        if skip.lower() == bad.lower():
            return False, f"classification {bad}"
    # Titles that suggest fragments/boxes/displays rather than objects
    tl = title.lower()
    for frag in ("fragment", "box for", "case for", "model of", "study for"):
        if frag in tl:
            return False, f"title contains '{frag}'"
    return True, ""


def guess_period(obj):
    """Convert Met objectDate to a display period + numeric sort year."""
    date = (obj.get("objectDate") or "").strip()
    culture = (obj.get("culture") or obj.get("dynasty") or obj.get("country") or "").strip()
    return date or "Undated", culture


def guess_region(obj):
    for key in ("country", "culture", "dynasty", "artistDisplayName", "region"):
        v = (obj.get(key) or "").strip()
        if v and key != "artistDisplayName":
            return v
        if v and key == "artistDisplayName":
            return v
    return obj.get("artistDisplayName", "Unknown") or "Unknown"


def clean_material(medium):
    if not medium:
        return "Mixed media"
    # Take the first clause, cap length
    m = medium.split(";")[0].split(".")[0].strip()
    return m if m else "Mixed media"


def clean_dimensions(d):
    if not d:
        return ""
    return d.split(";")[0].strip()


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    records = []
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH) as f:
            records = json.load(f)
    taken = {r["object_number"] for r in records}
    next_number = max(taken, default=0) + 1

    for category, queries in CATEGORY_QUERIES.items():
        got = sum(1 for r in records if r["category"] == category)
        print(f"\n=== {category} — have {got}, need {PER_CATEGORY}")
        for term, want in queries:
            if got >= PER_CATEGORY:
                break
            try:
                res = http_json(f"{API}/search?q={urllib.parse.quote(term)}&hasImages=true&medium=&isOnView=")
            except Exception as e:
                print(f"  search '{term}' failed: {e}")
                continue
            ids = (res.get("objectIDs") or [])[:60]
            print(f"  query '{term}': {len(ids)} candidates")
            for oid in ids:
                if got >= PER_CATEGORY:
                    break
                if any(r["met_object_id"] == oid for r in records):
                    continue
                try:
                    obj = http_json(f"{API}/objects/{oid}")
                except Exception as e:
                    print(f"    object {oid} failed: {e}")
                    continue
                ok, why = acceptable(obj)
                if not ok:
                    continue
                url = obj["primaryImage"]
                try:
                    raw = http_bytes(url)
                except Exception as e:
                    print(f"    {oid} download failed: {e}")
                    continue
                stage = normalize_to_stage(raw)
                n = next_number
                out_dir = os.path.join(OUT_ROOT, f"{n:03d}")
                os.makedirs(out_dir, exist_ok=True)
                out_path = os.path.join(out_dir, "00.webp")
                stage.save(out_path, "WEBP", quality=82, method=4)
                period, culture = guess_period(obj)
                year_raw = obj.get("objectDate", "")
                ys = None
                import re
                m2 = re.search(r"(1[0-9]{3}|20[0-2][0-9]|[5-9][0-9]{2}|b\.c\.|b\.c)", year_raw.lower())
                nums = re.findall(r"(?<!\d)([1-9][0-9]{2,3})(?!\d)", year_raw)
                if nums:
                    ys = int(nums[-1])
                    if "b.c" in year_raw.lower():
                        ys = -ys
                if ys is None:
                    ys = 1500
                record = {
                    "object_number": n,
                    "met_object_id": oid,
                    "name": obj["title"].strip(),
                    "subtitle": (obj.get("title") or "").strip()[:200],
                    "period": period,
                    "period_sort": ys,
                    "region": guess_region(obj),
                    "category": category,
                    "material": clean_material(obj.get("medium")),
                    "dimensions": clean_dimensions(obj.get("dimensions")),
                    "maker": (obj.get("artistDisplayName") or "Unsigned").strip() or "Unsigned",
                    "attribution": "",
                    "image_source": "The Metropolitan Museum of Art",
                    "image_source_url": obj.get("objectURL", ""),
                    "image_license": "Open Access CC0",
                    "image_credit": obj.get("creditLine", ""),
                    "accession": obj.get("accessionNumber", ""),
                    "gallery": obj.get("GalleryNumber", "") or "",
                }
                records.append(record)
                taken.add(n)
                next_number = n + 1
                got += 1
                print(f"    + No.{n:03d} [{category}] {record['name'][:58]} ({record['period']})")
                time.sleep(0.25)

    with open(JSON_PATH, "w") as f:
        json.dump(records, f, indent=2)
    print(f"\nSaved {len(records)} records → {JSON_PATH}")
    per_cat = {}
    for r in records:
        per_cat[r["category"]] = per_cat.get(r["category"], 0) + 1
    print(json.dumps(per_cat, indent=2))


if __name__ == "__main__":
    import urllib.parse
    main()
