"""Génère le gabarit du carrousel n°2 (post2_verdict.html), même charte que le n°1.

Usage : python carrousel/generer_post2.py
Dimanche soir : ouvrir post2_verdict.html, remplacer chaque [À REMPLIR] (surligné), puis
python carrousel/exporter.py carrousel/post2_verdict.html
"""
import json
from pathlib import Path

ICI = Path(__file__).parent
R = json.loads((ICI.parent / "resultats.json").read_text(encoding="utf-8"))
CSS = (ICI / "charte.css").read_text(encoding="utf-8")
TOTAL = 7
X = '<span class="a-remplir">[À REMPLIR]</span>'
mo = R["modele"]
pct = lambda x: f"{round(x * 100)}"
dec = lambda x: f"{x:.2f}".replace(".", ",")


def pied(n, source=""):
    s = f'<div class="source">{source}</div>' if source else ""
    return f'{s}<div class="pied"><span class="signature">Moïse Monnin · Data Analyst</span><span>{n}/{TOTAL}</span></div>'


BANDEAU = '<div class="bandeau"><span class="rayures"></span><span class="blanc-or"></span></div>'

s1 = f"""
<section class="slide split-diag">
  <div class="cote-barca rayures"></div><div class="cote-real"></div>
  <div class="etiquette-barca">FC Barcelone</div><div class="etiquette-real">Real Madrid</div>
  <div class="vs">VS</div>
  <!-- Accroche à adapter : favori gagnant → « Les stats avaient raison… cette fois. » -->
  <div class="carte-titre">
    <div class="kicker">Clásico · Le verdict</div>
    <h1>J'avais donné {pct(mo['barca'])} % au Barça.</h1>
    <p>Voici ce qui s'est passé. Modèle contre réalité : ce que les stats ont vu, et ce qu'elles ont raté.</p>
  </div>
  <div class="pied pied-clair"><span class="signature">Moïse Monnin · Data Analyst</span><span>Faites défiler →</span></div>
</section>"""

s2 = f"""
<section class="slide sans-marge">
  <div class="moitie moitie-barca rayures-sombres">
    <div class="kicker or-barca">FC Barcelone</div>
    <div class="geant or-barca">{X}</div>
    <div class="buts">Buteurs : {X}</div>
  </div>
  <div class="moitie moitie-real">
    <div class="kicker marine">Real Madrid</div>
    <div class="geant marine">{X}</div>
    <div class="buts">Buteurs : {X}</div>
  </div>
  <div class="medaillon"><span class="num" style="font-size:44px">FIN</span><span>score final</span></div>
  <div class="bas-sombre">
    <div class="kicker">Prédit contre réel</div>
    <h2>Prédit : {R['scores_probables'][0][0]} · Réel : {X}</h2>
    <p class="gris">Le modèle donnait <b class="num" style="color:var(--texte)">{X} %</b> de chances à ce score exact,
    et <b class="num" style="color:var(--texte)">{X} %</b> à cette issue (victoire / nul / défaite).</p>
    {pied(2, "Calcul : cellule « Après le match » du notebook.")}
  </div>
</section>"""

lignes = [("Buts", "barca", dec(mo["lambda_barca"])), ("Buts", "real", dec(mo["lambda_real"])),
          ("xG", "barca", "—"), ("xG", "real", "—"), ("Possession", "barca", "—"), ("Tirs cadrés", "barca", "—"), ("Tirs cadrés", "real", "—")]
rows = "".join(
    f'<tr><td><span class="pastille-club pc-{c}"></span>{lib} {"Barça" if c == "barca" else "Real"}</td>'
    f'<td class="num">{p}</td><td class="num">{X}</td></tr>' for lib, c, p in lignes)
s3 = f"""
<section class="slide">
  {BANDEAU}
  <div class="kicker">Prédit ou réel ?</div>
  <h2>Le match en chiffres.</h2>
  <table class="pvr"><tr><th></th><th>Prédit</th><th>Réel</th></tr>{rows}</table>
  <p class="gris" style="margin-top:34px; font-size:28px;">Les xG disent qui a mérité. Le score dit qui a marqué. Quand les deux divergent, c'est là que l'histoire se joue.</p>
  {pied(3, "Sources : ESPN (statistiques), Understat (xG) — relevés le 25/10/2026.")}
</section>"""


def panneau(club):
    cls = "barca" if club == "Barcelona" else "real"
    js = [j for j in R["joueurs"] if j["club"] == club]
    lignes = "".join(f'<tr><td class="joueur">{j["joueur"]}</td><td class="num">{dec(j["pendant"])}</td><td class="num">{X}</td></tr>' for j in js)
    return f'<div class="panneau panneau-{cls}"><table class="pvr pvr-panneau"><tr><th>Joueur</th><th>Moy. Clásico</th><th>Dimanche</th></tr>{lignes}</table></div>'


s4 = f"""
<section class="slide">
  {BANDEAU}
  <div class="kicker">Les joueurs suivis</div>
  <h2>Leur historique annonçait-il leur match&nbsp;?</h2>
  <p class="gris" style="font-size:25px; margin-bottom:20px;">Buts + passes décisives : moyenne par Clásico depuis 2021, puis dimanche.</p>
  {panneau("Barcelona")}{panneau("Real Madrid")}
  <p style="margin-top:18px; font-size:27px;">{X} — une phrase sur le joueur qui a confirmé ou démenti son historique.</p>
  {pied(4)}
</section>"""


def liste(n, kicker, titre, pistes):
    return f"""
<section class="slide">
  {BANDEAU}
  <div class="kicker">{kicker}</div>
  <h2>{titre}</h2>
  <ul class="limites"><li>{X}</li><li>{X}</li><li>{X}</li></ul>
  <div class="carte-neutre" style="margin-top:auto; margin-bottom:110px;"><p class="gris" style="font-size:25px;">Pistes : {pistes}</p></div>
  {pied(n)}
</section>"""


s5 = liste(5, "Ce que le modèle a vu", "Ce qui s'est vérifié.",
           "le favori, le nombre de buts (plus ou moins de 3), l'absence de nul (0 en 18 Clásicos), les joueurs « de grand match ».")
s6 = liste(6, "Ce que le modèle n'a pas vu", "Ce qui échappe aux chiffres.",
           "carton rouge, blessure en cours de match, penalty, but contre le cours du jeu, efficacité très supérieure aux xG.")

s7 = f"""
<section class="slide split-diag">
  <div class="cote-barca rayures"></div><div class="cote-real"></div>
  <div class="carte-titre carte-finale">
    <div class="kicker">La leçon</div>
    <h1 style="font-size:84px;">Les stats ont-elles dit la vérité&nbsp;?</h1>
    <p style="font-size:32px; color:var(--texte);">{X} — ta réponse nuancée en deux phrases.</p>
    <div class="appel">Un modèle ne prédit pas un match. <b>Il dit à quel point le résultat était surprenant.</b></div>
    <p class="petit">Merci à tous ceux qui ont joué le jeu en commentaire. Prochain Clásico : 9 mai 2027.</p>
  </div>
  <div class="pied pied-clair"><span class="signature">Moïse Monnin · Data Analyst</span><span>7/{TOTAL}</span></div>
</section>"""

EXTRA = """
.a-remplir { background: #FFE08A; color: #3B2A00; border-radius: 8px; padding: 0 10px; font-family: Inter; font-weight: 700; font-size: .6em; letter-spacing: 0; vertical-align: middle; }
.geant .a-remplir { font-size: 64px; }
table.pvr { width: 100%; border-collapse: collapse; font-size: 30px; }
table.pvr th { text-align: right; color: var(--gris); font: 700 22px Inter; text-transform: uppercase; letter-spacing: .12em; padding: 0 0 16px; }
table.pvr th:first-child { text-align: left; }
table.pvr td { padding: 18px 0; border-top: 1px solid var(--trait); }
table.pvr td.num { text-align: right; }
.pastille-club { display: inline-block; width: 22px; height: 22px; border-radius: 5px; margin-right: 16px; vertical-align: -2px; }
.pc-barca { background: linear-gradient(90deg, var(--fcb-bleu) 0 50%, var(--fcb-grenat) 50%); }
.pc-real { background: var(--rm-blanc); box-shadow: inset 0 -5px 0 var(--rm-or); }
.pvr-panneau { font-size: 28px; }
.pvr-panneau td { padding: 12px 0; border-top-color: rgba(127, 127, 127, .25); }
.panneau-real .pvr-panneau th { color: #4E6A93; }
.pvr-panneau .joueur { font-size: 32px; }
"""

html = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Clásico — Verdict data</title>
<!-- Gabarit généré par carrousel/generer_post2.py. Remplacer chaque [À REMPLIR] dimanche soir, directement ici. -->
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
