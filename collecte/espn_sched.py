"""Calendriers ESPN (toutes compétitions) du Barça (83) et du Real (86), saisons 2021 à 2026."""
import csv, json, sys, time, urllib.request
out = sys.argv[1]
TEAMS = {"Barcelona": 83, "Real Madrid": 86}
rows = []
def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})))
for club, tid in TEAMS.items():
    for season in range(2021, 2027):
        d = get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/all/teams/{tid}/schedule?season={season}")
        for e in d.get("events", []):
            lg = e.get("league", {}) or {}
            comp = e["competitions"][0]
            st = comp.get("status", {}).get("type", {})
            if not st.get("completed"): continue
            sides = {c["homeAway"]: c for c in comp["competitors"]}
            me = next(c for c in comp["competitors"] if str(c["team"]["id"]) == str(tid))
            other = next(c for c in comp["competitors"] if c is not me)
            sc = lambda c: c.get("score", {}).get("value") if isinstance(c.get("score"), dict) else c.get("score")
            rows.append({"club": club, "espn_id": e["id"], "date": e["date"][:10], "ligue_espn": lg.get("name", ""),
                         "slug": lg.get("slug", ""), "adversaire_espn": other["team"]["displayName"],
                         "domicile_espn": int(me["homeAway"] == "home"), "bp_espn": int(float(sc(me))), "bc_espn": int(float(sc(other)))})
        time.sleep(0.4)
seen = set(); uniq = []
for r in rows:
    k = (r["club"], r["espn_id"])
    if k not in seen: seen.add(k); uniq.append(r)
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(uniq[0])); w.writeheader(); w.writerows(uniq)
from collections import Counter
print(len(uniq), Counter(r["slug"] for r in uniq))
