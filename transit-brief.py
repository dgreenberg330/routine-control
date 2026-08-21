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
from datetime import datetime
from zoneinfo import ZoneInfo
from google.transit import gtfs_realtime_pb2

TZ = ZoneInfo("America/New_York")

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
# The L runs 8th Av <-> Canarsie. Verified against the realtime feed:
# L03S continues to L05/L06/L08/L10 (toward Lorimer/Canarsie) = Brooklyn-bound.
# L03N heads to L02/L01 (toward 8 Av) = Manhattan-bound. So Brooklyn-bound is "S".
L_STOP = "L03S"

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

# --- Departure-planning knobs (minutes) -----------------------------------
# The brief is generated at feed-fetch time but lands on the phone a few
# minutes later, so we emit wall-clock "leave-by" times (stable regardless of
# read delay) and drop any option that can't be made once delay + walk are
# counted.
MSG_LATENCY_MIN       = 5    # brief lands on phone ~5 min after generation
WALK_TO_6_MIN         = 5    # office -> 51 St platform
RIDE_6_MIN            = 10   # 51 St -> 14 St-Union Sq on the 6
TRANSFER_CUSHION_MIN  = 4    # min slack to make the L (3-5) & target wait
DEPART_SLACK_MIN      = 5    # don't recommend leaving tighter than this
MAX_TRANSFER_WAIT_MIN = 12   # flag pairings where you'd idle too long for the L


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
# Departure planning (couple the 6 to a catchable L, minimize transfer wait)
# --------------------------------------------------------------------------

def next_departure_ts(feed, stop_id, route_id, now, horizon_min=90):
    """Absolute unix timestamps of upcoming departures at stop_id on route_id."""
    if feed is None:
        return []

    out = []
    for entity in feed.entity:
        if not entity.HasField("trip_update"):
            continue

        tu = entity.trip_update
        if tu.trip.route_id != route_id:
            continue

        for stu in tu.stop_time_update:
            if stu.stop_id != stop_id:
                continue

            # Boarding cares about departure; fall back to arrival.
            ts = 0
            if stu.HasField("departure") and stu.departure.time:
                ts = stu.departure.time
            elif stu.HasField("arrival") and stu.arrival.time:
                ts = stu.arrival.time

            if ts and now <= ts <= now + horizon_min * 60:
                out.append(int(ts))

    return sorted(set(out))


def _clock(ts):
    return datetime.fromtimestamp(ts, TZ).strftime("%-I:%M%p").lower()


def _median_headway(ts_list):
    """Median gap (seconds) between successive departures, or None."""
    if len(ts_list) < 2:
        return None
    diffs = sorted(b - a for a, b in zip(ts_list, ts_list[1:]))
    return diffs[len(diffs) // 2]


def _match_l(ell, need, headway, max_project_min=30):
    """
    First L departing at/after `need`. Prefer a real-time prediction; if the
    need falls past the published L window, project forward from the last known
    L by its observed headway. Returns (timestamp, estimated_bool) or (None, _).
    """
    l_dep = next((t for t in ell if t >= need), None)
    if l_dep is not None:
        return l_dep, False
    if not ell or not headway:
        return None, False
    t = ell[-1]
    while t < need:
        t += headway
    if t - ell[-1] > max_project_min * 60:
        return None, False          # too far past real data to trust
    return t, True


def plan_departures(feed_num, feed_l, now):
    """
    For each downtown-6 departure at 51 St that is still catchable once the
    notification delay and walk are counted, find the first Brooklyn-bound L at
    Union Sq reachable with the transfer cushion, and record the L wait.
    """
    six = next_departure_ts(feed_num, SIX_STOP, "6", now)
    ell = next_departure_ts(feed_l, L_STOP, "L", now)
    if not six or not ell:
        return []

    l_headway = _median_headway(ell)
    earliest_leave = now + (MSG_LATENCY_MIN + DEPART_SLACK_MIN) * 60
    plans = []
    for d in six:
        leave = d - WALK_TO_6_MIN * 60
        if leave < earliest_leave:
            continue                                   # unmakeable after delay+walk
        arrive = d + RIDE_6_MIN * 60
        l_dep, est = _match_l(ell, arrive + TRANSFER_CUSHION_MIN * 60, l_headway)
        if l_dep is None:
            continue                                   # no L reachable, even projected
        plans.append({
            "leave": leave, "six": d, "arrive": arrive,
            "l": l_dep, "wait": int(round((l_dep - arrive) / 60)), "est": est,
        })
    return plans


def fmt_plan_lines(plans):
    if not plans:
        return ["When to leave: no catchable 6→L pairing in the feed window."]

    best = min((p["wait"] for p in plans if p["wait"] <= MAX_TRANSFER_WAIT_MIN),
               default=None)
    lines = ["When to leave (leave-by → 6 → L, minimizing L wait):"]
    for p in plans[:N_ARRIVALS]:
        star = " ⭐" if best is not None and p["wait"] == best else ""
        flag = " (long wait)" if p["wait"] > MAX_TRANSFER_WAIT_MIN else ""
        l_txt = f"~{_clock(p['l'])}" if p["est"] else _clock(p['l'])
        est = " (est. L)" if p["est"] else ""
        lines.append(
            f"• Leave {_clock(p['leave'])} → 6 @ {_clock(p['six'])} "
            f"→ L @ {l_txt} ({p['wait']} min transfer{est}){star}{flag}"
        )
    return lines


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

    lines = fmt_plan_lines(plan_departures(feed_num, feed_l, now))
    lines.append("")
    lines.append(fmt_arrivals("Next downtown 6 @ 51 St", six))
    lines.append(fmt_arrivals("Next L @ 14 St-Union Sq (Brooklyn-bound)", ell))

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
