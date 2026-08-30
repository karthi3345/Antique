#!/usr/bin/env python3
"""Top-up pass: fill under-quota categories with good Met CC0 objects.

Uses targeted, high-precision queries for the missing slots:
  - Scientific Instruments (needs 4 more; currently mostly clocks)
  - Metalwork (needs 6 more)
Strict validation as fetch_museum_archive. Incremental persist.
"""
import json
import os
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(__file__))
from fetch_museum_images import OUT_ROOT, DATA_DIR, JSON_PATH, http_bytes, normalize_to_stage  # noqa: E402
from fetch_museum_archive import (  # noqa: E402
    PER_CATEGORY, http_json_robust, valid_for, make_record,
)

EXTRA_SEARCHES = {
    "Scientific Instruments": [
        ("astrolabe planispheric", ""),
        ("quadrant", "14"),
        ("sundial", "14"),
        ("compass", "4"),
        ("armillary", ""),
        ("cross staff", ""),
        ("barometer", "12"),
        ("sector mathematical", ""),
        ("proportional compasses", ""),
        ("nocturnal", ""),
    ],
    "Metalwork": [
        ("tankard", "12"),
        ("ewer", "12"),
        ("aquamanile", "12"),
        ("basin", "12"),
        ("saltcellar", "12"),
        ("cup", "12"),
        ("beaker", "12"),
        ("chalice", "17"),
        ("censer", "14"),
        ("mortar", "12"),
    ],
}


def main():
    records = json.load(open(JSON_PATH))
    existing_ids = {r["met_object_id"] for r in records}
    next_number = max(r["object_number"] for r in records) + 1

    def persist():
        json.dump(records, open(JSON_PATH, "w"), indent=2)

    for category, searches in EXTRA_SEARCHES.items():
        got = sum(1 for r in records if r["category"] == category)
        print(f"=== {category}: have {got}")
        for term, dept in searches:
            if got >= PER_CATEGORY:
                break
            q = (f"https://collectionapi.metmuseum.org/public/collection/v1/search"
                 f"?q={urllib.parse.quote(term)}&hasImages=true"
                 + (f"&departmentIds={dept}" if dept else ""))
            try:
                res = http_json_robust(q)
            except Exception as e:
                print(f"  search '{term}' failed {e}")
                continue
            for oid in (res or {}).get("objectIDs") or []:
                if got >= PER_CATEGORY:
                    break
                if oid in existing_ids:
                    continue
                try:
                    obj = http_json_robust(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{oid}")
                except Exception:
                    continue
                if not obj or not valid_for(obj, category):
                    time.sleep(0.12)
                    continue
                try:
                    raw = http_bytes(obj["primaryImage"])
                except Exception as e:
                    print(f"  img {oid} failed {e}")
                    continue
                stage = normalize_to_stage(raw)
                out_dir = os.path.join(OUT_ROOT, f"{next_number:03d}")
                os.makedirs(out_dir, exist_ok=True)
                stage.save(os.path.join(out_dir, "00.webp"), "WEBP", quality=82, method=4)
                rec = make_record(obj, category, next_number)
                records.append(rec)
                existing_ids.add(oid)
                persist()
                next_number += 1
                got += 1
                print(f"  + No.{rec['object_number']:03d} {rec['name'][:50]} ({rec['period'][:22]})")
                time.sleep(0.35)

    import collections
    print(json.dumps(collections.Counter(r["category"] for r in records), indent=2))


if __name__ == "__main__":
    main()
