"""Génère le carrousel n°2 (post2_verdict.html) : le modèle face au résultat du 25/10/2026.

Usage : python carrousel/generer_post2.py   puis   python carrousel/exporter.py carrousel/post2_verdict.html
Les chiffres viennent de resultats.json (notebook) et de data/match_25102026.json (Flashscore).
"""
import json
from pathlib import Path

ICI = Path(__file__).parent
R = json.loads((ICI.parent / "resultats.json").read_text(encoding="utf-8"))
M = json.loads((ICI.parent / "data" / "match_25102026.json").read_text(encoding="utf-8"))
CSS = (ICI / "charte.css").read_text(encoding="utf-8")
TOTAL = 7
mo, ve, st = R["modele"], R["verdict"], M["stats"]
pct = lambda x: f"{round(x * 100)}"
dec = lambda x, n=2: f"{x:.{n}f}".replace(".", ",")
SOURCE_MATCH = "Sources : Flashscore (statistiques du match), modèle publié le 25/10/2026 avant le coup d'envoi."


def pied(n, source=""):
    s = f'<div class="source">{source}</div>' if source else ""
    return f'{s}<div class="pied"><span class="signature">Moïse Monnin · Data Analyst</span><span>{n}/{TOTAL}</span></div>'


def buteurs(equipe):
    return ", ".join(f"{b['buteur'].split()[-1]} {b['minute']}'" for b in M["buts"] if b["equipe"] == equipe)


BANDEAU = '<div class="bandeau"><span class="rayures"></span><span class="blanc-or"></span></div>'

# 1 · Accroche
s1 = f"""
<section class="slide split-diag">
  <div class="cote-barca rayures"></div><div class="cote-real"></div>
  <div class="etiquette-barca">FC Barcelone</div><div class="etiquette-real">Real Madrid</div>
  <div class="vs">{M['score']['barca']}-{M['score']['real']}</div>
  <div class="carte-titre">
    <div class="kicker">Clásico · Le verdict</div>
    <h1>J'avais donné {pct(ve['proba_issue_modele'])} % au Real.<br><span class="txt-real">Il a gagné.</span></h1>
    <p>Barça {M['score']['barca']}-{M['score']['real']} Real. Ce que les stats avaient vu, et ce qu'elles ont raté.</p>
  </div>
  <div class="pied pied-clair"><span class="signature">Moïse Monnin · Data Analyst</span><span>Faites défiler →</span></div>
</section>"""

# 2 · Le score, chaque camp à sa charte
s2 = f"""
<section class="slide sans-marge">
  <div class="moitie moitie-barca rayures-sombres">
    <div class="kicker or-barca">FC Barcelone</div>
    <div class="geant or-barca">{M['score']['barca']}</div>
    <div class="buts">{buteurs('Barcelona')}</div>
  </div>
  <div class="moitie moitie-real">
    <div class="kicker marine">Real Madrid</div>
    <div class="geant marine">{M['score']['real']}</div>
    <div class="buts">{buteurs('Real Madrid')}</div>
  </div>
  <div class="medaillon"><span class="num" style="font-size:52px">FIN</span><span>25.10.26</span></div>
  <div class="bas-sombre">
    <div class="kicker">Prédit contre réel</div>
    <h2>Prédit : {R['scores_probables'][0][0]} · Réel : {ve['score']}</h2>
    <p class="gris">Le modèle donnait <b class="num" style="color:var(--texte)">{pct(ve['proba_score'])} %</b> à ce score
    ({ve['rang_score']}<sup>e</sup> plus probable) et <b class="num" style="color:var(--texte)">{pct(ve['proba_issue_modele'])} %</b> à une victoire du Real.
    Le marché : {pct(ve['proba_issue_marche'])} %.</p>
    {pied(2, SOURCE_MATCH)}
  </div>
</section>"""

# 3 · Prédit ou réel
lignes = [("barca", "Buts attendus Barça", dec(mo["lambda_barca"]), dec(st["xg"][0]) + " xG"),
          ("real", "Buts attendus Real", dec(mo["lambda_real"]), dec(st["xg"][1]) + " xG"),
          ("barca", "Possession Barça", "—", f"{st['possession'][0]} %"),
          ("barca", "Tirs Barça (cadrés)", "—", f"{st['tirs'][0]} ({st['tirs_cadres'][0]})"),
          ("real", "Tirs Real (cadrés)", "—", f"{st['tirs'][1]} ({st['tirs_cadres'][1]})"),
          ("barca", "Grosses occasions Barça", "—", str(st["grosses_occasions"][0])),
          ("real", "Grosses occasions Real", "—", str(st["grosses_occasions"][1]))]
rows = "".join(f'<tr><td><span class="pastille-club pc-{c}"></span>{lib}</td><td class="num">{p}</td><td class="num">{r}</td></tr>'
               for c, lib, p, r in lignes)
s3 = f"""
<section class="slide">
  {BANDEAU}
  <div class="kicker">Prédit ou réel ?</div>
  <h2>Le Barça a eu le ballon. Le Real, les occasions.</h2>
  <table class="pvr"><tr><th></th><th>Prédit</th><th>Réel</th></tr>{rows}</table>
  <p style="margin-top:30px; font-size:28px;">Selon les xG, la victoire du Real n'a rien d'un hold-up : <b>il a créé plus et mieux</b>, avec 8 tirs de moins.</p>
  {pied(3, "Buts attendus prédits : modèle de Poisson. Réel : expected goals (xG) du match, Flashscore.")}
</section>"""

# 4 · Les joueurs
def panneau(club):
    cls = "barca" if club == "Barcelona" else "real"
    js = [j for j in R["joueurs"] if j["club"] == club]
    lignes = "".join(
        f'<tr><td class="joueur">{j["joueur"]}</td><td class="num">{dec(j["pendant"])}</td>'
        f'<td class="num">{M["joueurs_bp"][j["joueur"]]}{" ✓" if M["joueurs_bp"][j["joueur"]] >= 1 else ""}</td></tr>' for j in js)
    return f'<div class="panneau panneau-{cls}"><table class="pvr pvr-panneau"><tr><th>Joueur</th><th>Moy. Clásico</th><th>Dimanche</th></tr>{lignes}</table></div>'


s4 = f"""
<section class="slide">
  {BANDEAU}
  <div class="kicker">Les joueurs suivis</div>
  <h2>Les joueurs de grand match ont tenu leur rang.</h2>
  <p class="gris" style="font-size:25px; margin-bottom:20px;">Buts + passes décisives : moyenne par Clásico depuis 2021, puis dimanche.</p>
  {panneau("Barcelona")}{panneau("Real Madrid")}
  <p style="margin-top:18px; font-size:27px;"><b class="txt-real">Mbappé</b>, déjà le plus décisif de l'historique, a doublé la mise : 2 buts. <b class="txt-barca">Raphinha</b> a marqué, comme son historique l'annonçait.</p>
  {pied(4, "Sources : ESPN (historique), Flashscore (25/10/2026).")}
</section>"""


def liste(n, kicker, titre, items, conclusion):
    lis = "".join(f"<li><b>{a}</b> <span class='gris'>{b}</span></li>" for a, b in items)
    return f"""
<section class="slide">
  {BANDEAU}
  <div class="kicker">{kicker}</div>
  <h2>{titre}</h2>
  <ul class="limites">{lis}</ul>
  <div class="carte-neutre" style="margin-top:auto; margin-bottom:110px;"><p>{conclusion}</p></div>
  {pied(n)}
</section>"""


s5 = liste(5, "Ce que le modèle a vu", "Ce qui s'est vérifié.", [
    ("Pas de match nul.", "La série continue : 0 nul en 19 Clásicos. Le modèle n'y donnait que 20 %."),
    ("Un match à 3 buts.", "Le total le plus probable selon le modèle (22 %)."),
    ("Les joueurs décisifs.", "Mbappé et Raphinha, les deux meilleurs rendements en Clásico, ont marqué."),
], "Le modèle avait bien lu <b>la nature du match</b> : ouvert, sans nul, porté par ses stars.")

s6 = liste(6, "Ce que le modèle n'a pas vu", "Ce qui échappe aux chiffres.", [
    ("Une attaque du Barça éteinte.", f"{dec(st['xg'][0])} xG produits, moitié moins que les {dec(mo['lambda_barca'])} buts attendus."),
    ("Un Real plus dangereux que prévu.", f"{dec(st['xg'][1])} xG au lieu de {dec(mo['lambda_real'])}, et 4 grosses occasions contre 2."),
    ("La forme n'a pas suffi.", "Le Barça, plus en forme, a perdu : 11 victoires sur 19 pour l'équipe la plus en forme (58 %)."),
], "Ni chance ni malchance : chaque équipe a marqué à peu près ses xG. <b>Le modèle s'est trompé sur le match, pas sur la finition.</b>")

s7 = f"""
<section class="slide split-diag">
  <div class="cote-barca rayures"></div><div class="cote-real"></div>
  <div class="carte-titre carte-finale">
    <div class="kicker">La leçon</div>
    <h1 style="font-size:84px;">Les stats ont-elles dit la vérité&nbsp;?</h1>
    <p style="font-size:31px; color:var(--texte);">Oui et non. Le Real n'avait qu'1 chance sur 5 avant le match. Mais pendant le match, les chiffres ont parlé pour lui.</p>
    <div class="appel">Un modèle ne prédit pas un match. <b>Il dit à quel point le résultat était surprenant. Ici : 1 chance sur 5.</b></div>
    <p class="petit">Merci à tous ceux qui ont joué le jeu. Prochain Clásico : 9 mai 2027.</p>
  </div>
  <div class="pied pied-clair"><span class="signature">Moïse Monnin · Data Analyst</span><span>7/{TOTAL}</span></div>
</section>"""

EXTRA = """
table.pvr { width: 100%; border-collapse: collapse; font-size: 29px; }
table.pvr th { text-align: right; color: var(--gris); font: 700 22px Inter; text-transform: uppercase; letter-spacing: .12em; padding: 0 0 16px; }
table.pvr th:first-child { text-align: left; }
table.pvr td { padding: 17px 0; border-top: 1px solid var(--trait); }
table.pvr td.num { text-align: right; }
.pastille-club { display: inline-block; width: 22px; height: 22px; border-radius: 5px; margin-right: 16px; vertical-align: -2px; }
.pc-barca { background: linear-gradient(90deg, var(--fcb-bleu) 0 50%, var(--fcb-grenat) 50%); }
.pc-real { background: var(--rm-blanc); box-shadow: inset 0 -5px 0 var(--rm-or); }
.pvr-panneau { font-size: 28px; }
.pvr-panneau td { padding: 12px 0; border-top-color: rgba(127, 127, 127, .25); }
.panneau-real .pvr-panneau th { color: #4E6A93; }
.pvr-panneau .joueur { font-size: 32px; }
.split-diag .vs { font-size: 70px; }
"""

html = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Clásico — Verdict data</title>
<!-- Fichier généré par carrousel/generer_post2.py à partir de resultats.json et data/match_25102026.json. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
{CSS}
{EXTRA}
</style>
</head>
<body>
{s1}{s2}{s3}{s4}{s5}{s6}{s7}
</body>
</html>
"""
(ICI / "post2_verdict.html").write_text(html, encoding="utf-8")
print("post2_verdict.html généré")
