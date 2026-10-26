"""Génère clasico_analyse.ipynb à partir des cellules ci-dessous (texte + code).

Usage : python collecte/generer_notebook.py
Modifier le notebook ici plutôt qu'à la main garde une seule source de vérité.
"""
import json, os

CELLS = []
md = lambda s: CELLS.append(("markdown", s.strip("\n")))
code = lambda s: CELLS.append(("code", s.strip("\n")))

md(r"""
# Clásico FC Barcelone – Real Madrid · 25 octobre 2026
## Les stats diront-elles la vérité ?

**Auteur :** Moïse Monnin — Data Analyst

Ce notebook part des **preuves** (18 Clásicos officiels depuis octobre 2021) pour arriver à un **pronostic chiffré**.
Chaque étape est expliquée en français simple.

> **Comment l'utiliser dans Google Colab :** clique sur une cellule de code puis appuie sur **Shift + Entrée**.
> Exécute les cellules dans l'ordre, de haut en bas.

*Analyse à but pédagogique — ceci n'est pas un conseil de pari.*
""")

md(r"""
## 1. Préparer les outils

`pandas` sert à manipuler des tableaux de données (comme Excel, mais en code),
`numpy` à faire des calculs, `matplotlib` à dessiner les graphiques.
""")
code(r"""
import json, math, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Les données sont lues sur place si elles existent, sinon depuis GitHub (cas de Google Colab).
DEPOT = "https://raw.githubusercontent.com/MOSESCI/clasico-data-2026/main/data/"
SOURCE = "data/" if os.path.exists("data/matchs.csv") else DEPOT
os.makedirs("graphiques", exist_ok=True)

DATE_MATCH = "2026-10-25"
BARCA, REAL = "Barcelona", "Real Madrid"

# Charte graphique : fond sombre, une couleur par club (palette vérifiée pour les daltoniens)
FOND, ENCRE, GRIS = "#1A1A19", "#F2F0EA", "#9A978F"
COULEUR = {BARCA: "#E0457B", REAL: "#B8891F", "Nul": "#6E6C66"}
plt.rcParams.update({
    "figure.facecolor": FOND, "axes.facecolor": FOND, "savefig.facecolor": FOND,
    "text.color": ENCRE, "axes.labelcolor": GRIS, "xtick.color": GRIS, "ytick.color": GRIS,
    "axes.edgecolor": "#3A3936", "font.size": 13, "axes.spines.top": False, "axes.spines.right": False,
})
print("Données lues depuis :", SOURCE)
""")

md(r"""
## 2. Charger les données

Quatre fichiers, collectés et vérifiés en amont (voir le dossier `collecte/`) :

| Fichier | Contenu | Source |
|---|---|---|
| `matchs.csv` | Tous les matchs officiels du Barça et du Real depuis 2021 (score, compétition, xG en Liga) | ESPN, contrôlé avec Wikipédia ; xG : Understat |
| `buts.csv` | Chaque but : buteur et passeur décisif | ESPN |
| `presences.csv` | Si les 6 joueurs suivis ont joué chaque match | ESPN |
| `liga_*.csv` | Tous les matchs de Liga 2025-26 et 2026-27 | ESPN |
""")
code(r"""
matchs = pd.read_csv(SOURCE + "matchs.csv")
buts = pd.read_csv(SOURCE + "buts.csv")
presences = pd.read_csv(SOURCE + "presences.csv")
liga = pd.concat([pd.read_csv(SOURCE + "liga_2025_26.csv"), pd.read_csv(SOURCE + "liga_2026_27.csv")])

# Points gagnés à chaque match : victoire 3, nul 1, défaite 0
matchs["points"] = np.select([matchs.buts_pour > matchs.buts_contre, matchs.buts_pour == matchs.buts_contre], [3, 1], 0)
matchs["diff_buts"] = matchs.buts_pour - matchs.buts_contre
print(len(matchs), "matchs officiels chargés")
matchs.tail()
""")

md(r"""
### Contrôle qualité

Chaque score ESPN a été comparé à celui de Wikipédia. La colonne `controle_wikipedia` indique le résultat.
""")
code(r"""
print(matchs.controle_wikipedia.value_counts())
assert (matchs.controle_wikipedia != "ECART").all(), "Un score diffère entre les deux sources : à vérifier !"

# Le nombre de buts détaillés (buteurs) doit correspondre au score final de chaque match
detail = buts.groupby("espn_id").size()
verif = matchs.drop_duplicates("espn_id").set_index("espn_id")
verif = verif[verif.index.isin(detail.index)]
assert (detail[verif.index] == verif.buts_pour + verif.buts_contre).all()
print("Contrôle réussi : scores identiques dans les deux sources, buts détaillés complets.")
""")

md(r"""
## 3. Le bilan historique (1902 – 2026)

Source : Wikipédia, *List of El Clásico matches* (matchs officiels jusqu'au 10 mai 2026).
""")
code(r"""
BILAN = {"matchs": 264, "victoires_real": 106, "nuls": 52, "victoires_barca": 106, "buts_real": 444, "buts_barca": 441}
print(f"{BILAN['matchs']} Clásicos officiels : {BILAN['victoires_barca']} victoires du Barça, "
      f"{BILAN['victoires_real']} du Real, {BILAN['nuls']} nuls. Buts : {BILAN['buts_barca']} – {BILAN['buts_real']}.")
""")

md(r"""
## 4. Les 18 derniers Clásicos et la forme avant chacun

**Forme** = points pris et différence de buts sur les **5 matchs officiels précédents** (toutes compétitions).
Exemple : 4 victoires et 1 nul = 13 points sur 15.
""")
code(r"""
def forme(club, avant_le, n=5):
    # Les n derniers matchs officiels d'un club avant une date
    m = matchs[(matchs.club == club) & (matchs.date < avant_le)].sort_values("date").tail(n)
    return {"points": int(m.points.sum()), "diff_buts": int(m.diff_buts.sum()),
            "xg_diff": round((m.xg_pour - m.xg_contre).sum(), 2), "resultats": "".join(m.points.map({3: "V", 1: "N", 0: "D"}))}

clasicos = matchs[(matchs.club == BARCA) & (matchs.adversaire == REAL)].sort_values("date").copy()
lignes = []
for _, c in clasicos.iterrows():
    fb, fr = forme(BARCA, c.date), forme(REAL, c.date)
    lignes.append({"date": c.date, "competition": c.competition, "score": f"{c.buts_pour}-{c.buts_contre}",
                   "vainqueur": BARCA if c.buts_pour > c.buts_contre else REAL if c.buts_pour < c.buts_contre else "Nul",
                   "forme_barca": fb["points"], "db_barca": fb["diff_buts"], "forme_real": fr["points"], "db_real": fr["diff_buts"],
                   "ecart_buts_clasico": c.buts_pour - c.buts_contre, "espn_id": c.espn_id})
histo = pd.DataFrame(lignes)

# L'équipe « en meilleure forme » : plus de points ; à égalité, meilleure différence de buts
def plus_en_forme(r):
    a, b = (r.forme_barca, r.db_barca), (r.forme_real, r.db_real)
    return BARCA if a > b else REAL if b > a else "Égalité"
histo["plus_en_forme"] = histo.apply(plus_en_forme, axis=1)
histo
""")

md(r"""
## 5. Preuve n°1 — l'équipe la plus en forme gagne-t-elle le Clásico ?
""")
code(r"""
comparables = histo[histo.plus_en_forme != "Égalité"]
gagne = (comparables.plus_en_forme == comparables.vainqueur).sum()
nuls = (comparables.vainqueur == "Nul").sum()
perd = len(comparables) - gagne - nuls
taux = gagne / len(comparables)
print(f"L'équipe la plus en forme a gagné {gagne} Clásicos sur {len(comparables)} ({taux:.0%}), "
      f"en a perdu {perd}, nuls : {nuls}.")

# Est-ce mieux que le hasard ? Probabilité d'obtenir au moins ce score en tirant à pile ou face
p_hasard = sum(math.comb(len(comparables), k) for k in range(gagne, len(comparables) + 1)) / 2 ** len(comparables)
print(f"Probabilité d'un tel résultat par pur hasard (pile ou face) : {p_hasard:.0%}")

# L'écart de forme prédit-il l'écart au score ? (corrélation : 1 = parfait, 0 = aucun lien)
correlation = np.corrcoef(histo.forme_barca - histo.forme_real, histo.ecart_buts_clasico)[0, 1]
print(f"Corrélation entre l'écart de forme et l'écart au score : {correlation:.2f}")
""")

md(r"""
**Lecture :** la forme désigne le vainqueur un peu plus souvent que le hasard, mais avec seulement 18 matchs
ce n'est pas une preuve solide. Et l'**ampleur** de l'écart de forme ne dit presque rien de l'ampleur du score.
""")
code(r"""
fig, ax = plt.subplots(figsize=(6.4, 2.5))
for i, r in histo.iterrows():
    ax.add_patch(plt.Rectangle((i + 0.06, 0.06), 0.88, 0.88, color=COULEUR[r.vainqueur], lw=0))
    signe = "✓" if r.plus_en_forme == r.vainqueur else "✗"
    ax.text(i + 0.5, 0.5, signe, ha="center", va="center", fontsize=17, color=FOND, weight="bold")
    ax.text(i + 0.5, -0.24, r.score, ha="center", va="center", fontsize=9, color=ENCRE, rotation=90)
ax.text(0.06, 1.2, "Oct. 2021", ha="left", va="center", fontsize=10, color=GRIS)
ax.text(len(histo) - 0.06, 1.2, "Mai 2026 →", ha="right", va="center", fontsize=10, color=GRIS)
ax.set_xlim(0, len(histo)); ax.set_ylim(-0.55, 1.35); ax.axis("off")
ax.text(0, -0.6, "Couleur = vainqueur (rose Barça, doré Real)  ·  ✓ = la plus en forme a gagné", fontsize=10, color=GRIS, va="top")
plt.savefig("graphiques/preuve_forme.png", dpi=200, bbox_inches="tight")
plt.show()
""")

md(r"""
## 6. Les joueurs : la forme avant le Clásico annonce-t-elle leur match ?

Six attaquants titulaires probables dimanche (Vinícius Júnior est suspendu).
Mesure : **buts + passes décisives (B+P) par match joué**, sur les 5 matchs précédents puis pendant le Clásico.
""")
code(r"""
JOUEURS = {BARCA: ["Lamine Yamal", "Raphinha", "Fermín López"], REAL: ["Kylian Mbappé", "Jude Bellingham", "Arda Güler"]}

def contributions(joueur, espn_id):
    # Buts + passes décisives d'un joueur dans un match
    b = buts[buts.espn_id == espn_id]
    return int((b.buteur == joueur).sum() + (b.passeur == joueur).sum())

def a_joue(joueur, espn_id):
    p = presences[(presences.espn_id == espn_id) & (presences.joueur == joueur)]
    return len(p) > 0 and p.a_joue.iloc[0] == 1

lignes = []
for club, noms in JOUEURS.items():
    for joueur in noms:
        for _, c in histo.iterrows():
            if not a_joue(joueur, c.espn_id):
                continue
            avant = matchs[(matchs.club == club) & (matchs.date < c.date)].sort_values("date").tail(5)
            joues = [e for e in avant.espn_id if a_joue(joueur, e)]
            if not joues:
                continue
            lignes.append({"club": club, "joueur": joueur, "date": c.date,
                           "bp_avant_par_match": sum(contributions(joueur, e) for e in joues) / len(joues),
                           "bp_clasico": contributions(joueur, c.espn_id)})
perf = pd.DataFrame(lignes)
resume = perf.groupby(["club", "joueur"]).agg(clasicos=("date", "count"), avant=("bp_avant_par_match", "mean"),
                                              pendant=("bp_clasico", "mean")).round(2)
resume["ecart"] = (resume.pendant - resume.avant).round(2)
correlation_joueurs = np.corrcoef(perf.bp_avant_par_match, perf.bp_clasico)[0, 1]
print(f"Corrélation forme avant / rendement pendant le Clásico (tous joueurs) : {correlation_joueurs:.2f}")
resume
""")
code(r"""
ordre = [j for c in (BARCA, REAL) for j in JOUEURS[c] if j in resume.index.get_level_values(1)][::-1]
fig, ax = plt.subplots(figsize=(6.4, 4.4))
for y, joueur in enumerate(ordre):
    club = BARCA if joueur in JOUEURS[BARCA] else REAL
    r = resume.loc[(club, joueur)]
    ax.plot([r.avant, r.pendant], [y, y], color="#3A3936", lw=2, zorder=1)
    ax.scatter(r.avant, y, s=110, facecolor=FOND, edgecolor=COULEUR[club], lw=2.5, zorder=2)
    ax.scatter(r.pendant, y, s=110, color=COULEUR[club], edgecolor=FOND, lw=2, zorder=3)
    ax.text(-0.04, y, f"{joueur} ({int(r.clasicos)})", ha="right", va="center", fontsize=13, color=ENCRE)
ax.set_yticks([]); ax.spines["left"].set_visible(False)
ax.set_xlim(0, max(resume.avant.max(), resume.pendant.max()) + 0.25)
ax.set_xlabel("Buts + passes décisives par match")
ax.grid(axis="x", color="#2C2B29", lw=1); ax.set_axisbelow(True)
ax.scatter([], [], s=90, facecolor=FOND, edgecolor=GRIS, lw=2, label="5 matchs avant")
ax.scatter([], [], s=90, color=GRIS, label="Pendant le Clásico")
ax.legend(loc="upper center", bbox_to_anchor=(0.45, 1.12), ncol=2, frameon=False, fontsize=11, handletextpad=0.2, columnspacing=1)
plt.savefig("graphiques/joueurs.png", dpi=200, bbox_inches="tight")
plt.show()
""")

md(r"""
## 7. La forme actuelle (5 derniers matchs avant dimanche)
""")
code(r"""
actuelle = {}
for club in (BARCA, REAL):
    f = forme(club, DATE_MATCH)
    derniers = matchs[(matchs.club == club) & (matchs.date < DATE_MATCH)].sort_values("date").tail(5)
    f["matchs"] = [f"{r.adversaire} {r.buts_pour}-{r.buts_contre} ({r.competition})" for r in derniers.itertuples()]
    actuelle[club] = f
    print(club, "→", f["resultats"], "|", f["points"], "pts sur 15 | diff. de buts", f"{f['diff_buts']:+d}")
    for x in f["matchs"]:
        print("    ", x)
""")

md(r"""
## 8. Le pronostic : un modèle de Poisson

**L'idée :** le nombre de buts d'une équipe dans un match suit à peu près une *loi de Poisson* —
on peut calculer la probabilité de marquer 0, 1, 2, 3… buts à partir d'une moyenne attendue (λ, « lambda »).

**Comment on calcule λ :**
1. **Force d'attaque** = buts marqués par match ÷ moyenne de la Liga.
2. **Force de défense** = buts encaissés par match ÷ moyenne de la Liga.
3. λ Barça = attaque Barça × défense Real × moyenne des buts à domicile en Liga (le match est au Camp Nou).
4. λ Real = attaque Real × défense Barça × moyenne des buts à l'extérieur.

On utilise les **38 derniers matchs de Liga** de chaque équipe (une saison glissante) : 9 matchs seulement
cette saison, c'est trop peu pour être fiable.
""")
code(r"""
moy_dom, moy_ext = liga.buts_dom.mean(), liga.buts_ext.mean()
moy = (moy_dom + moy_ext) / 2

def forces(club, colonne_pour="buts_pour", colonne_contre="buts_contre", n=38):
    m = matchs[(matchs.club == club) & (matchs.competition == "Liga") & (matchs.date < DATE_MATCH)].sort_values("date").tail(n)
    return m[colonne_pour].mean() / moy, m[colonne_contre].mean() / moy

def poisson(k, lam):
    return math.exp(-lam) * lam ** k / math.factorial(k)

def pronostic(att_b, def_b, att_r, def_r):
    lam_b, lam_r = att_b * def_r * moy_dom, att_r * def_b * moy_ext
    grille = np.array([[poisson(i, lam_b) * poisson(j, lam_r) for j in range(11)] for i in range(11)])
    return {"lambda_barca": lam_b, "lambda_real": lam_r,
            "barca": np.tril(grille, -1).sum(), "nul": np.trace(grille), "real": np.triu(grille, 1).sum(), "grille": grille}

att_b, def_b = forces(BARCA); att_r, def_r = forces(REAL)
modele = pronostic(att_b, def_b, att_r, def_r)
print(f"Buts attendus : Barça {modele['lambda_barca']:.2f} – Real {modele['lambda_real']:.2f}")
print(f"Victoire Barça {modele['barca']:.0%} | Nul {modele['nul']:.0%} | Victoire Real {modele['real']:.0%}")

g = modele["grille"]
top = sorted(((g[i, j], f"{i}-{j}") for i in range(11) for j in range(11)), reverse=True)[:5]
print("Scores les plus probables :", ", ".join(f"{s} ({p:.0%})" for p, s in top))
""")

md(r"""
### Vérification de robustesse : le même modèle avec les xG

Les *expected goals* (xG) mesurent la qualité des occasions plutôt que les buts réellement marqués.
Si les deux versions vont dans le même sens, le pronostic est plus solide.
""")
code(r"""
xatt_b, xdef_b = forces(BARCA, "xg_pour", "xg_contre"); xatt_r, xdef_r = forces(REAL, "xg_pour", "xg_contre")
modele_xg = pronostic(xatt_b, xdef_b, xatt_r, xdef_r)
print(f"Version xG — Barça {modele_xg['barca']:.0%} | Nul {modele_xg['nul']:.0%} | Real {modele_xg['real']:.0%}")
""")

md(r"""
### Le modèle face au marché

Les cotes sont converties en **probabilités implicites** (1 ÷ cote), puis on retire la marge des opérateurs
pour que le total fasse 100 %. Moyenne de 4 opérateurs (relevé du 21/10/2026). Aucun opérateur n'est cité.
""")
code(r"""
cotes = pd.read_csv(SOURCE + "cotes.csv")

def proba_americaine(c):
    # Cote « américaine » : -170 = favori, +310 = outsider
    return -c / (-c + 100) if c < 0 else 100 / (c + 100)

implicites = cotes[["barca", "nul", "real"]].map(proba_americaine)
implicites = implicites.div(implicites.sum(axis=1), axis=0)   # on retire la marge
marche = implicites.mean()
print(f"Marché — Barça {marche.barca:.0%} | Nul {marche.nul:.0%} | Real {marche.real:.0%}")
""")
code(r"""
fig, ax = plt.subplots(figsize=(6.4, 2.6))
series = [("Modèle (buts)", modele), ("Modèle (xG)", modele_xg), ("Marché", {"barca": marche.barca, "nul": marche.nul, "real": marche.real})]
for y, (nom, p) in enumerate(series[::-1]):
    gauche = 0
    for cle, club in (("barca", BARCA), ("nul", "Nul"), ("real", REAL)):
        ax.barh(y, p[cle] - 0.004, left=gauche, color=COULEUR[club], height=0.62)
        ax.text(gauche + p[cle] / 2, y, f"{p[cle]:.0%}", ha="center", va="center", fontsize=13, color=FOND if club != "Nul" else ENCRE, weight="bold")
        gauche += p[cle]
    ax.text(-0.01, y, nom, ha="right", va="center", fontsize=13, color=ENCRE)
ax.set_xlim(0, 1); ax.axis("off")
for x, t, ha in ((0.0, "Victoire Barça", "left"), (modele["barca"] + modele["nul"] / 2, "Nul", "center"), (1.0, "Victoire Real", "right")):
    ax.text(x, 2.6, t, ha=ha, fontsize=11, color=GRIS)
plt.savefig("graphiques/pronostic.png", dpi=200, bbox_inches="tight")
plt.show()
""")

md(r"""
### Après le match (pour le post du lundi)

Le résultat et les statistiques du match sont dans `data/match_25102026.json` (source : Flashscore).
On mesure à quel point le résultat était surprenant pour le modèle, et si le match a ressemblé à la prédiction.
""")
code(r"""
try:
    with open(SOURCE.replace(DEPOT, "data/") + "match_25102026.json", encoding="utf-8") as f:
        MATCH = json.load(f)
except FileNotFoundError:
    import urllib.request
    MATCH = json.load(urllib.request.urlopen(DEPOT + "match_25102026.json"))

b, r = MATCH["score"]["barca"], MATCH["score"]["real"]
issue = "barca" if b > r else "real" if r > b else "nul"
rang = sorted((g[i, j] for i in range(11) for j in range(11)), reverse=True).index(g[b, r]) + 1
xg_b, xg_r = MATCH["stats"]["xg"]
verdict = {"score": f"{b}-{r}", "issue": issue, "proba_score": round(float(g[b, r]), 3), "rang_score": rang,
           "proba_issue_modele": round(float(modele[issue]), 3), "proba_issue_xg": round(float(modele_xg[issue]), 3),
           "proba_issue_marche": round(float(marche[issue]), 3), "xg": [xg_b, xg_r]}
print(f"Score réel {b}-{r} : le modèle lui donnait {g[b, r]:.1%} de chances ({rang}e score le plus probable).")
print(f"L'issue « {issue} » : modèle {modele[issue]:.0%}, version xG {modele_xg[issue]:.0%}, marché {marche[issue]:.0%}.")
print(f"Buts attendus avant le match : {modele['lambda_barca']:.2f} – {modele['lambda_real']:.2f} | xG réels : {xg_b} – {xg_r}")
""")

md(r"""
## 9. Exporter les chiffres clés

Ces chiffres alimentent le carrousel LinkedIn. Les sauvegarder dans un fichier évite les erreurs de recopie.
""")
code(r"""
resultats = {
    "bilan": BILAN,
    "preuve_forme": {"gagne": int(gagne), "perd": int(perd), "nuls": int(nuls), "sur": int(len(comparables)),
                     "taux": round(float(taux), 3), "p_hasard": round(float(p_hasard), 3), "correlation": round(float(correlation), 2),
                     "nuls_sur_18": int((histo.vainqueur == "Nul").sum())},
    "clasicos": histo[["date", "competition", "score", "vainqueur", "plus_en_forme"]].to_dict("records"),
    "joueurs": resume.reset_index().to_dict("records"), "correlation_joueurs": round(float(correlation_joueurs), 2),
    "forme_actuelle": actuelle,
    "modele": {k: round(float(modele[k]), 3) for k in ("lambda_barca", "lambda_real", "barca", "nul", "real")},
    "modele_xg": {k: round(float(modele_xg[k]), 3) for k in ("barca", "nul", "real")},
    "scores_probables": [(s, round(float(p), 3)) for p, s in top],
    "marche": {k: round(float(v), 3) for k, v in marche.items()},
    "verdict": verdict,
}
with open("resultats.json", "w", encoding="utf-8") as f:
    json.dump(resultats, f, ensure_ascii=False, indent=2)
print(json.dumps(resultats["modele"], indent=2))
""")

md(r"""
## 10. Les limites (à lire avant de conclure)

- **Petit échantillon :** 18 Clásicos, c'est peu. Un résultat à 61 % peut être dû au hasard.
- **Le modèle ignore** les blessures et suspensions (Vinícius, Olmo…), la fatigue, le contexte émotionnel et l'arbitrage.
- **Poisson suppose** que les buts des deux équipes sont indépendants ; en réalité, un but change le match.
- **Les xG** ne sont disponibles qu'en Liga dans nos données.

> Les statistiques décrivent des **tendances** sur beaucoup de matchs. Un seul match reste une épreuve du hasard.
> C'est tout l'enjeu de la question : *les stats diront-elles la vérité ?* Réponse lundi.
""")

nb = {"nbformat": 4, "nbformat_minor": 5,
      "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                   "language_info": {"name": "python"}, "colab": {"provenance": []}},
      "cells": []}
for i, (kind, src) in enumerate(CELLS):
    cell = {"cell_type": kind, "id": f"c{i:02d}", "metadata": {}, "source": src.splitlines(keepends=True)}
    if kind == "code":
        cell.update(execution_count=None, outputs=[])
    nb["cells"].append(cell)
dest = os.path.join(os.path.dirname(__file__), "..", "clasico_analyse.ipynb")
json.dump(nb, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Notebook écrit :", os.path.abspath(dest), "-", len(CELLS), "cellules")
