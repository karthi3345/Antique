#!/usr/bin/env python3
"""Fetch pass 3: strict global cleanup + fill + renumber to a clean 1..56.

Every existing record is re-validated against the strict rules (department,
classification, title). Failures are dropped. Then we fetch replacements with
strict checks, and finally renumber all records sequentially 1..56, moving
image directories to match.
"""
import json
import os
import re
import time
import urllib.parse

import sys
sys.path.insert(0, os.path.dirname(__file__))
from fetch_museum_images import (  # noqa: E402
    API, OUT_ROOT, JSON_PATH, PER_CATEGORY,
    http_json, http_bytes, normalize_to_stage,
)
from fetch_museum_pass2 import (  # noqa: E402
    QUERIES, TITLE_BLOCKLIST, GOOD_DEPARTMENTS, CATEGORY_MATCH,
)


def title_ok(t):
    tl = t.lower()
    return not any(b in tl for b in TITLE_BLOCKLIST)


def dept_ok(obj):
    return (obj.get("department") or "").strip() in GOOD_DEPARTMENTS


def class_ok(obj, category):
    cl = (obj.get("classification") or "").strip().lower()
    if not cl:
        return False
    return any(k in cl for k in CATEGORY_MATCH[category])


def record_ok(r):
    # local sanity: title + category plausibility
    if not title_ok(r["name"]):
        return False
    return True


def fetch_object_meta(oid):
    return http_json(f"{API}/objects/{oid}")


def main():
    records = json.load(open(JSON_PATH))

    # 1. Validate every record against the Met API once more
    keep = []
    dropped = []
    for r in records:
        try:
            obj = fetch_object_meta(r["met_object_id"])
        except Exception:
            obj = {}
        if not obj:
            # cannot verify — keep only if title passes
            if record_ok(r):
                keep.append(r)
            else:
                dropped.append((r["object_number"], r["name"], "unverifiable"))
            continue
        ok = (obj.get("isPublicDomain")
              and title_ok(obj.get("title", ""))
              and dept_ok(obj)
              and class_ok(obj, r["category"]))
        if ok:
            keep.append(r)
        else:
            dropped.append((r["object_number"], obj.get("title") or r["name"],
                            f"dept={obj.get('department')!r} class={obj.get('classification')!r}"))
        time.sleep(0.15)
    print(f"Dropped {len(dropped)}:")
    for d in dropped:
        print("  -", d)

    # 2. Count per category, fetch replacements (strict)
    counts = {}
    for r in keep:
        counts[r["category"]] = counts.get(r["category"], 0) + 1
    existing_ids = {r["met_object_id"] for r in keep}
    next_number = max(r["object_number"] for r in keep) + 1 if keep else 1

    for category, queries in QUERIES.items():
        got = counts.get(category, 0)
        if got >= PER_CATEGORY:
            continue
        print(f"\n=== {category} — have {got}, need {PER_CATEGORY - got}")
        for term in queries:
            if got >= PER_CATEGORY:
                break
            try:
                res = http_json(f"{API}/search?q={urllib.parse.quote(term)}&hasImages=true")
            except Exception:
                continue
            for oid in (res.get("objectIDs") or [])[:100]:
                if got >= PER_CATEGORY:
                    break
                if oid in existing_ids:
                    continue
                try:
                    obj = fetch_object_meta(oid)
                except Exception:
                    continue
                if not (obj.get("isPublicDomain") and obj.get("primaryImage")):
                    continue
                if not (title_ok(obj.get("title", "")) and dept_ok(obj) and class_ok(obj, category)):
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
                keep.append({
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
                })
                existing_ids.add(oid)
                counts[category] = got = got + 1
                next_number = n + 1
                print(f"  + No.{n:03d} [{category}] {obj['title'][:52]} ({date[:26]})")
                time.sleep(0.2)

    print("\nAfter fill:", json.dumps({k: sum(1 for r in keep if r['category'] == k) for k in QUERIES}))

    # 3. Renumber sequentially 1..N and move image dirs
    keep.sort(key=lambda r: (list(QUERIES).index(r["category"]), r["period_sort"], r["object_number"]))
    mapping = {}
    for i, r in enumerate(keep, start=1):
        mapping[r["object_number"]] = i
    # do moves in two phases to avoid collisions
    tmp_moves = []
    for r in keep:
        old = os.path.join(OUT_ROOT, f"{r['object_number']:03d}")
        new = os.path.join(OUT_ROOT, f"tmp_{mapping[r['object_number']]:03d}")
        if os.path.isdir(old):
            os.rename(old, new)
            tmp_moves.append((new, os.path.join(OUT_ROOT, f"{mapping[r['object_number']]:03d}")))
    for old_tmp, final in tmp_moves:
        os.rename(old_tmp, final)
    for r in keep:
        r["object_number"] = mapping[r["object_number"]]

    # remove stale dirs from the legacy 36-frame era (not referenced anymore)
    referenced = {f"{r['object_number']:03d}" for r in keep}
    for d in os.listdir(OUT_ROOT):
        if d not in referenced:
            full = os.path.join(OUT_ROOT, d)
            if os.path.isdir(full):
                for f in os.listdir(full):
                    os.remove(os.path.join(full, f))
                os.rmdir(full)
                print("removed stale", d)

    json.dump(keep, open(JSON_PATH, "w"), indent=2)
    print(f"\nFinal: {len(keep)} objects")
    for r in keep:
        print(f"{r['object_number']:03d} [{r['category'][:14]:14s}] {r['name'][:50]:50s} {r['period'][:26]}")


if __name__ == "__main__":
    main()
