#!/usr/bin/env python3
"""Fetch pass 4 (final): drop invalid records, fill categories to 8, renumber 1..56.

Robust renumbering: build the new list first, then move dirs via a staging area,
never overwriting. Strict validation: CC0, object departments only,
classification must match the category, title blocklist.
"""
import json
import os
import re
import shutil
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(__file__))
from fetch_museum_images import (  # noqa: E402
    API, OUT_ROOT, JSON_PATH, PER_CATEGORY,
    http_json, http_bytes, normalize_to_stage,
)
from fetch_museum_pass2 import (  # noqa: E402
    QUERIES, TITLE_BLOCKLIST, GOOD_DEPARTMENTS, CATEGORY_MATCH,
)

CATEGORY_ORDER = list(QUERIES)


def title_ok(t):
    tl = (t or "").lower()
    return not any(b in tl for b in TITLE_BLOCKLIST)


def valid_for(obj, category):
    if not obj.get("isPublicDomain") or not obj.get("primaryImage"):
        return False
    if not title_ok(obj.get("title", "")):
        return False
    if (obj.get("department") or "").strip() not in GOOD_DEPARTMENTS:
        return False
    cl = (obj.get("classification") or "").strip().lower()
    if not cl:
        return False
    return any(k in cl for k in CATEGORY_MATCH[category])


def make_record(obj, category, n):
    date = (obj.get("objectDate") or "").strip() or "Undated"
    nums = re.findall(r"(?<!\d)([1-9][0-9]{2,3})(?!\d)", date)
    ys = int(nums[-1]) if nums else 1500
    if "b.c" in date.lower():
        ys = -abs(ys)
    region = (obj.get("culture") or obj.get("country") or obj.get("dynasty") or "").strip()
    if not region:
        region = (obj.get("artistDisplayName") or "Unknown").strip()
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
        "image_source": "The Metropolitan Museum of Art",
        "image_source_url": obj.get("objectURL", ""),
        "image_license": "Open Access CC0",
        "image_credit": obj.get("creditLine", ""),
        "accession": obj.get("accessionNumber", ""),
        "gallery": obj.get("GalleryNumber", "") or "",
    }


def save_image(obj, n):
    raw = http_bytes(obj["primaryImage"])
    stage = normalize_to_stage(raw)
    out_dir = os.path.join(OUT_ROOT, f"{n:03d}")
    os.makedirs(out_dir, exist_ok=True)
    stage.save(os.path.join(out_dir, "00.webp"), "WEBP", quality=82, method=4)


def main():
    records = json.load(open(JSON_PATH))

    # -- 1. Validate each record against the Met API -----------------------
    valid = []
    for r in records:
        try:
            obj = http_json(f"{API}/objects/{r['met_object_id']}")
        except Exception:
            continue
        if valid_for(obj, r["category"]):
            valid.append((r, obj))
        time.sleep(0.1)
    print(f"validated {len(valid)} / {len(records)} existing records")

    # -- 2. Fill categories to 8 -------------------------------------------
    counts = {}
    for r, _ in valid:
        counts[r["category"]] = counts.get(r["category"], 0) + 1
    existing_ids = {r["met_object_id"] for r, _ in valid}
    next_number = 100  # fresh high range, renumbered later

    for category in CATEGORY_ORDER:
        got = counts.get(category, 0)
        if got >= PER_CATEGORY:
            continue
        print(f"=== {category}: have {got}")
        for term in QUERIES[category]:
            if got >= PER_CATEGORY:
                break
            try:
                res = http_json(
                    f"{API}/search?q={urllib.parse.quote(term)}&hasImages=true")
            except Exception:
                continue
            for oid in (res.get("objectIDs") or [])[:120]:
                if got >= PER_CATEGORY:
                    break
                if oid in existing_ids:
                    continue
                try:
                    obj = http_json(f"{API}/objects/{oid}")
                except Exception:
                    continue
                if not valid_for(obj, category):
                    continue
                try:
                    save_image(obj, next_number)
                except Exception as e:
                    print(f"  dl fail {oid}: {e}")
                    continue
                rec = make_record(obj, category, next_number)
                valid.append((rec, obj))
                existing_ids.add(oid)
                counts[category] = got = got + 1
                print(f"  + tmp{next_number:03d} [{category}] {rec['name'][:50]} ({rec['period'][:24]})")
                next_number += 1
                time.sleep(0.2)

    final = [r for r, _ in valid]

    # -- 3. Order by category then period, renumber 1..N -------------------
    final.sort(key=lambda r: (CATEGORY_ORDER.index(r["category"]), r["period_sort"], r["met_object_id"]))
    staging = os.path.join(os.path.dirname(OUT_ROOT), "objects_staging")
    if os.path.exists(staging):
        shutil.rmtree(staging)
    os.makedirs(staging)
    for i, r in enumerate(final, start=1):
        src = os.path.join(OUT_ROOT, f"{r['object_number']:03d}", "00.webp")
        dst = os.path.join(staging, f"{i:03d}")
        os.makedirs(dst, exist_ok=True)
        shutil.copy2(src, os.path.join(dst, "00.webp"))
        r["object_number"] = i

    # swap staging into place
    shutil.rmtree(OUT_ROOT)
    shutil.move(staging, OUT_ROOT)

    json.dump(final, open(JSON_PATH, "w"), indent=2)
    print(f"\nFinal: {len(final)} objects in 1..{len(final)}")
    c = {}
    for r in final:
        c[r["category"]] = c.get(r["category"], 0) + 1
    print(json.dumps(c, indent=2))
    for r in final:
        print(f"{r['object_number']:03d} [{r['category'][:14]:14s}] {r['name'][:48]:48s} {r['period'][:26]}")


if __name__ == "__main__":
    main()
