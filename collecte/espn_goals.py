"""Pour chaque Clásico (et celui du 25/10/2026), récupère buteurs + passeurs (ESPN) des 5 matchs précédents de chaque club et du Clásico lui-même."""
import csv, json, sys, time, urllib.request
import pandas as pd
raw = sys.argv[1]
e = pd.read_csv(raw + "/espn_calendrier.csv")
e = e[~e.slug.isin(["club.friendly", "esp.joan_gamper"])].sort_values("date")
clas = e[(e.club == "Barcelona") & (e.adversaire_espn == "Real Madrid")]
dates = list(clas.date) + ["2026-10-25"]
need = set(clas.espn_id)
for d in dates:
    for club in ("Barcelona", "Real Madrid"):
        need |= set(e[(e.club == club) & (e.date < d)].tail(5).espn_id)
print("matchs a detailler:", len(need))
rows = []
for i, eid in enumerate(sorted(need)):
    slug = e[e.espn_id == eid].slug.iloc[0]
    url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/summary?event={eid}"
    d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})))
    for k in d.get("keyEvents", []):
        if not k.get("scoringPlay"): continue
        typ = k["type"]["text"]; parts = [p["athlete"]["displayName"] for p in k.get("participants", [])]
        own = "Own Goal" in typ
        rows.append({"espn_id": eid, "minute": k.get("clock", {}).get("displayValue", ""), "type": typ,
                     "equipe": k.get("team", {}).get("displayName", ""),
                     "buteur": "" if own else (parts[0] if parts else ""),
                     "passeur": parts[1] if len(parts) > 1 and not own and "Penalty" not in typ else ""})
    time.sleep(0.3)
with open(raw + "/espn_buts.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), "buts")
