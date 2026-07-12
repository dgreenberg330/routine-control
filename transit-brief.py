#!/usr/bin/env python3
"""
Evening commute transit brief.

Route: downtown 6 from 51st St -> transfer 14th St-Union Sq -> L -> Lorimer St.

Emits a plain-text block suitable for dropping into a Telegram message.
Prints nothing to stdout on hard failure except a fallback line, so the
parent routine never dies on an MTA hiccup.

Requires:
    pip install gtfs-realtime-bindings requests --break-system-packages

Network:
    api-endpoint.mta.info must be in the egress allowlist.

Stop IDs are VERIFIED-BY-DEFAULT-OFF. Run verify_stops.py once against the
static GTFS stops.txt and hard-code the results below before trusting output.
"""

import time
import sys
import requests
from google.transit import gtfs_realtime_pb2

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------

BASE = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds"

FEED_NUMBERED = f"{BASE}/nyct%2Fgtfs"     # 1 2 3 4 5 6 7 S  -> the 6
FEED_L = f"{BASE}/nyct%2Fgtfs-l"          # L

# --- Stop IDs -------------------------------------------------------------
# Suffix N/S is DIRECTION, not compass. It follows the feed's own convention,
# which is not always intuitive. Verify with verify_stops.py.
#
# 51st St (Lexington Ave line), downtown/Brooklyn-bound 6.
SIX_STOP = "630S"
#
# 14th St-Union Sq (Canarsie line), Brooklyn-bound L.
# The L runs 8th Av <-> Canarsie. Brooklyn-bound may be "N" on this line.
# THIS IS THE MOST LIKELY THING TO BE WRONG. Verify it.
L_STOP = "L03N"

# Stations on the L between Union Sq and Lorimer St, inclusive. Used to decide
# whether an L alert actually touches the leg of the line being ridden.
# Base station IDs (no direction suffix).
L_SEGMENT_STATIONS = {
    "L03",  # 14 St-Union Sq
    "L05",  # 3 Av
    "L06",  # 1 Av
    "L08",  # Bedford Av
    "L10",  # Lorimer St
}

SIX_SEGMENT_STATIONS = {
    "630",  # 51 St
    "631",  # Grand Central-42 St
    "632",  # 33 St
    "633",  # 28 St
    "634",  # 23 St
    "635",  # 14 St-Union Sq
}

N_ARRIVALS = 4          # how many upcoming trains to show per line
MIN_MINUTES = 1         # ignore trains already effectively departed
TIMEOUT = 15


# --------------------------------------------------------------------------
# Feed access
# --------------------------------------------------------------------------

def fetch_feed(url):
    """Fetch and parse a GTFS-RT feed. Returns FeedMessage or None."""
    try:
        resp = requests.get(url, timeout=TIMEOUT)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"[warn] feed fetch failed {url}: {exc}", file=sys.stderr)
        return None

    feed = gtfs_realtime_pb2.FeedMessage()
    try:
        feed.ParseFromString(resp.content)
    except Exception as exc:  # protobuf raises a grab-bag of types
        print(f"[warn] feed parse failed {url}: {exc}", file=sys.stderr)
        return None
    return feed


# --------------------------------------------------------------------------
# Arrivals
# --------------------------------------------------------------------------

def next_arrivals(feed, stop_id, route_id, now=None, limit=N_ARRIVALS):
    """Minutes-from-now for the next trains at stop_id on route_id."""
    if feed is None:
        return []

    now = now or time.time()
    mins = []

    for entity in feed.entity:
        if not entity.HasField("trip_update"):
            continue

        tu = entity.trip_update
        if tu.trip.route_id != route_id:
            continue

        for stu in tu.stop_time_update:
            if stu.stop_id != stop_id:
                continue

            # Prefer arrival; some updates carry only departure.
            ts = 0
            if stu.HasField("arrival") and stu.arrival.time:
                ts = stu.arrival.time
            elif stu.HasField("departure") and stu.departure.time:
                ts = stu.departure.time
            if not ts:
                continue

            delta = (ts - now) / 60.0
            if delta >= MIN_MINUTES:
                mins.append(int(round(delta)))

    return sorted(set(mins))[:limit]


# --------------------------------------------------------------------------
# Alerts
# --------------------------------------------------------------------------

def _alert_text(alert):
    """Pull the English header out of an alert, best effort."""
    for field in (alert.header_text, alert.description_text):
        for tr in field.translation:
            if tr.text and tr.text.strip():
                return " ".join(tr.text.split())
    return ""


def relevant_alerts(feed, route_id, segment_stations):
    """
    Alerts on route_id that plausibly touch the segment being ridden.

    Filtering logic:
      - Alert must name route_id in an informed_entity.
      - If any informed_entity carries stop_ids for this route, at least one
        must fall inside segment_stations. This is what keeps a Canarsie-end
        L problem out of a Union Sq -> Lorimer commute.
      - If the alert carries NO stop_ids at all, it is route-wide and we keep
        it, because we cannot rule it out.
    """
    if feed is None:
        return []

    out = []

    for entity in feed.entity:
        if not entity.HasField("alert"):
            continue

        alert = entity.alert

        names_route = False
        stops_on_route = set()

        for ie in alert.informed_entity:
            if ie.route_id != route_id:
                continue
            names_route = True
            if ie.stop_id:
                # Strip the trailing direction char to get the station.
                base = ie.stop_id[:-1] if ie.stop_id[-1] in "NS" else ie.stop_id
                stops_on_route.add(base)

        if not names_route:
            continue

        if stops_on_route and not (stops_on_route & segment_stations):
            # Alert is scoped to stations outside the commute leg.
            continue

        text = _alert_text(alert)
        if text:
            out.append(text)

    # De-dupe; the MTA repeats the same alert across entities.
    seen = set()
    deduped = []
    for t in out:
        if t not in seen:
            seen.add(t)
            deduped.append(t)
    return deduped


# --------------------------------------------------------------------------
# Render
# --------------------------------------------------------------------------

def fmt_arrivals(label, mins):
    if not mins:
        return f"{label}: no upcoming trains reported"
    return f"{label}: " + ", ".join(f"{m} min" for m in mins)


def build_brief():
    now = time.time()

    feed_num = fetch_feed(FEED_NUMBERED)
    feed_l = fetch_feed(FEED_L)

    if feed_num is None and feed_l is None:
        return "Transit: MTA feeds unavailable."

    six = next_arrivals(feed_num, SIX_STOP, "6", now=now)
    ell = next_arrivals(feed_l, L_STOP, "L", now=now)

    lines = [
        fmt_arrivals("Downtown 6 @ 51 St", six),
        fmt_arrivals("L @ 14 St-Union Sq (Brooklyn-bound)", ell),
    ]

    alerts = []
    alerts += [("6", t) for t in relevant_alerts(feed_num, "6", SIX_SEGMENT_STATIONS)]
    alerts += [("L", t) for t in relevant_alerts(feed_l, "L", L_SEGMENT_STATIONS)]

    # Per the routine spec: if nothing survives the filter, say nothing at all.
    if alerts:
        lines.append("")
        for route, text in alerts:
            lines.append(f"{route}: {text}")

    return "\n".join(lines)


if __name__ == "__main__":
    print(build_brief())
