"""Présence (titulaire / entré en jeu) des 6 joueurs suivis dans chaque match détaillé + résultats Liga 2026-27."""
import csv, json, sys, time, urllib.request
import pandas as pd
raw = sys.argv[1]
JOUEURS = ["Lamine Yamal", "Raphinha", "Fermín López", "Kylian Mbappé", "Jude Bellingham", "Arda Güler"]
get = lambda u: json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})))
e = pd.read_csv(raw + "/espn_calendrier.csv").drop_duplicates("espn_id").set_index("espn_id")
ids = sorted(set(pd.read_csv(raw + "/espn_buts.csv").espn_id) | set(e[(e.bp_espn + e.bc_espn) == 0].index))
# matchs à 0-0 parmi ceux nécessaires : on les reprend tous, le filtrage se fait dans le notebook
rows = []
for eid in ids:
    if e.loc[eid, "slug"] in ("club.friendly", "esp.joan_gamper"): continue
    d = get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{e.loc[eid,'slug']}/summary?event={eid}")
    for team in d.get("rosters", []):
        for p in team.get("roster", []):
            n = p.get("athlete", {}).get("displayName", "")
            if n in JOUEURS:
                rows.append({"espn_id": eid, "joueur": n, "titulaire": int(bool(p.get("starter"))),
                             "a_joue": int(bool(p.get("starter")) or bool(p.get("subbedIn")))})
    time.sleep(0.25)
with open(raw + "/espn_presences.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["espn_id", "joueur", "titulaire", "a_joue"]); w.writeheader(); w.writerows(rows)
print(len(ids), "matchs,", len(rows), "lignes presence")
# Liga 2026-27 : tous les matchs joués (moyennes de buts de la ligue pour le modèle)
sb = get("https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/scoreboard?dates=20260801-20261024&limit=400")
L = []
for ev in sb["events"]:
    c = ev["competitions"][0]
    if not c["status"]["type"]["completed"]: continue
    h = next(x for x in c["competitors"] if x["homeAway"] == "home"); a = next(x for x in c["competitors"] if x["homeAway"] == "away")
    L.append({"date": ev["date"][:10], "domicile": h["team"]["displayName"], "exterieur": a["team"]["displayName"],
              "buts_dom": int(h["score"]), "buts_ext": int(a["score"])})
with open(raw + "/liga_2026_27.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(L[0])); w.writeheader(); w.writerows(L)
print(len(L), "matchs de Liga 2026-27")
