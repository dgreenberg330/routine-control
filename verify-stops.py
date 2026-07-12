#!/usr/bin/env python3
"""
One-time stop ID verification.

The stop IDs hard-coded in transit_brief.py were written from memory and are
NOT trustworthy. Run this once against the MTA static GTFS stops.txt to
confirm or correct them, then edit transit_brief.py accordingly.

Get stops.txt from the MTA developer downloads (static GTFS bundle for NYCT
subway), unzip, and point this at it:

    python verify_stops.py /path/to/stops.txt

What you are looking for:
  - The parent station row for each station (stop_id with no N/S suffix)
  - The two child rows, <id>N and <id>S, which are the direction platforms
  - Confirm which of N/S is the direction you actually ride

The N/S suffix is a feed convention, not a compass bearing. On the L in
particular, do not assume Brooklyn-bound is "S".
"""

import csv
import sys

TARGETS = {
    "51 St": "downtown 6 origin",
    "14 St-Union Sq": "6 -> L transfer",
    "Lorimer St": "L destination",
    "Bedford Av": "L, sanity check",
    "1 Av": "L, sanity check",
}


def main(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))

    print(f"{len(rows)} stop rows loaded\n")

    for name, why in TARGETS.items():
        print(f"=== {name}  ({why})")
        hits = [r for r in rows if r.get("stop_name", "").strip() == name]
        if not hits:
            # Fall back to substring, station names vary in punctuation.
            hits = [
                r for r in rows
                if name.lower().replace("-", " ")
                in r.get("stop_name", "").lower().replace("-", " ")
            ]
        if not hits:
            print("  NO MATCH — check exact spelling in stops.txt\n")
            continue

        for r in sorted(hits, key=lambda x: x["stop_id"]):
            sid = r["stop_id"]
            parent = r.get("parent_station", "")
            kind = "parent" if not parent else f"platform of {parent}"
            print(f"  {sid:<8} {r['stop_name']:<28} {kind}")
        print()

    print("-" * 60)
    print("Now edit transit_brief.py:")
    print("  SIX_STOP  -> the 51 St platform for DOWNTOWN 6")
    print("  L_STOP    -> the Union Sq platform for BROOKLYN-BOUND L")
    print()
    print("If you cannot tell which suffix is which from stops.txt alone,")
    print("run transit_brief.py with each and see which returns arrivals")
    print("that move in the right direction over a couple of minutes.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
