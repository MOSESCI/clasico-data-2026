"""Résultats de Liga entre deux dates (moyennes de la ligue pour le modèle de Poisson).

Usage : python espn_liga.py <sortie.csv> <debut AAAA-MM-JJ> <fin AAAA-MM-JJ>"""
import csv, json, sys, time, urllib.request
from datetime import date, timedelta
out = sys.argv[1]
get = lambda u: json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})))
debut, fin = (date.fromisoformat(x) for x in sys.argv[2:4])
L, seen, d = [], set(), debut
while d <= fin:
    f = d
    sb = get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/scoreboard?dates={d:%Y%m%d}")
    for ev in sb["events"]:
        c = ev["competitions"][0]
        if not c["status"]["type"]["completed"] or ev["id"] in seen: continue
        seen.add(ev["id"])
        h = next(x for x in c["competitors"] if x["homeAway"] == "home"); a = next(x for x in c["competitors"] if x["homeAway"] == "away")
        L.append({"date": ev["date"][:10], "domicile": h["team"]["displayName"], "exterieur": a["team"]["displayName"],
                  "buts_dom": int(h["score"]), "buts_ext": int(a["score"])})
    d = f + timedelta(days=1); time.sleep(0.15)
with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(L[0])); w.writeheader(); w.writerows(L)
print(len(L), "matchs")
