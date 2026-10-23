"""Assemble les fichiers bruts (Wikipédia, ESPN, Understat) en jeux de données propres dans data/.

Usage : python collecte/construire_donnees.py <dossier_brut>
"""
import glob, json, os, sys
import pandas as pd

raw = sys.argv[1]
out = os.path.join(os.path.dirname(__file__), "..", "data")
COMP = {"esp.1": "Liga", "uefa.champions": "Ligue des champions", "esp.copa_del_rey": "Coupe du Roi",
        "esp.super_cup": "Supercoupe d'Espagne", "uefa.europa": "Ligue Europa", "fifa.cwc": "Mondial des clubs",
        "fifa.intercontinental_cup": "Coupe intercontinentale", "uefa.super_cup": "Supercoupe d'Europe"}

# 1. Matchs officiels (ESPN) + contrôle des scores avec Wikipédia
e = pd.read_csv(f"{raw}/espn_calendrier.csv")
e = e[e.slug.isin(COMP)].drop_duplicates(["club", "espn_id"]).copy()
e["competition"] = e.slug.map(COMP)
w = pd.read_csv(f"{raw}/matchs.csv")[["club", "date", "buts_pour", "buts_contre"]]
m = e.merge(w, on=["club", "date"], how="left")
m["controle_wikipedia"] = "absent"
ok = m.buts_pour.notna()
m.loc[ok, "controle_wikipedia"] = ((m.buts_pour == m.bp_espn) & (m.buts_contre == m.bc_espn)).map({True: "identique", False: "ECART"})[ok]
m["neutre"] = m.slug.isin(["esp.super_cup", "fifa.cwc", "fifa.intercontinental_cup", "uefa.super_cup"]) | (
    (m.slug == "esp.copa_del_rey") & m.adversaire_espn.eq("Real Madrid") & m.date.eq("2025-04-26"))
m = m.rename(columns={"adversaire_espn": "adversaire", "domicile_espn": "domicile", "bp_espn": "buts_pour", "bc_espn": "buts_contre"}) \
     .drop(columns=["buts_pour_x", "buts_contre_x", "ligue_espn"], errors="ignore")
m = m.rename(columns={"buts_pour_y": "_wp", "buts_contre_y": "_wc"}).drop(columns=["_wp", "_wc"], errors="ignore")

# 2. xG Understat (Liga uniquement)
xg = []
for fn in glob.glob(f"{raw}/us_*_*.json"):
    club = "Barcelona" if "Barcelona" in fn else "Real Madrid"
    for d in json.load(open(fn, encoding="utf-8"))["dates"]:
        if not d["isResult"]: continue
        me, ot = ("h", "a") if d["side"] == "h" else ("a", "h")
        xg.append({"club": club, "date": d["datetime"][:10], "xg_pour": round(float(d["xG"][me]), 2), "xg_contre": round(float(d["xG"][ot]), 2)})
xg = pd.DataFrame(xg).drop_duplicates(["club", "date"])
m = m.merge(xg, on=["club", "date"], how="left")
m.loc[m.competition != "Liga", ["xg_pour", "xg_contre"]] = None
cols = ["club", "date", "competition", "adversaire", "domicile", "neutre", "buts_pour", "buts_contre", "xg_pour", "xg_contre", "espn_id", "controle_wikipedia"]
m = m[cols].sort_values(["club", "date"])
m.to_csv(f"{out}/matchs.csv", index=False)

# 3. Buts et passes décisives (ESPN), présences des 6 joueurs suivis
g = pd.read_csv(f"{raw}/espn_buts.csv")
g.to_csv(f"{out}/buts.csv", index=False)
pd.read_csv(f"{raw}/espn_presences.csv").drop_duplicates(["espn_id", "joueur"]).to_csv(f"{out}/presences.csv", index=False)

# 4. Liga 2026-27 (tous les clubs)
pd.read_csv(f"{raw}/liga_2026_27.csv").to_csv(f"{out}/liga_2026_27.csv", index=False)
print(m.controle_wikipedia.value_counts().to_dict(), "| xG Liga:", m.xg_pour.notna().sum(), "/", (m.competition == "Liga").sum())
