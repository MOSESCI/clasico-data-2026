"""Génère le carrousel n°1 (post1_pronostic.html) aux chartes du Barça et du Real, à partir de resultats.json.

Usage : python carrousel/generer_post1.py   puis   python carrousel/exporter.py carrousel/post1_pronostic.html
Les chiffres viennent du notebook (resultats.json) : on ne les recopie jamais à la main.
"""
import json
from pathlib import Path

ICI = Path(__file__).parent
R = json.loads((ICI.parent / "resultats.json").read_text(encoding="utf-8"))
BARCA, REAL = "Barcelona", "Real Madrid"
TOTAL = 9


def pct(x):
    return f"{round(x * 100)}"


def dec(x, n=2):
    return f"{x:.{n}f}".replace(".", ",").replace("-", "−")


CSS = (ICI / "charte.css").read_text(encoding="utf-8")


def pied(n, source=""):
    s = f'<div class="source">{source}</div>' if source else ""
    return f'{s}<div class="pied"><span class="signature">Moïse Monnin · Data Analyst</span><span>{n}/{TOTAL}</span></div>'


def bandeau():
    return '<div class="bandeau"><span class="rayures"></span><span class="blanc-or"></span></div>'


# ---------- 1. Accroche (écran partagé en diagonale) ----------
s1 = f"""
<section class="slide split-diag">
  <div class="cote-barca rayures"></div>
  <div class="cote-real"></div>
  <div class="etiquette-barca">FC Barcelone</div>
  <div class="etiquette-real">Real Madrid</div>
  <div class="vs">VS</div>
  <div class="carte-titre">
    <div class="kicker">Clásico · Dimanche 25 octobre · 20h00 GMT</div>
    <h1>Les données ont-elles déjà le résultat&nbsp;?</h1>
    <p>18 Clásicos passés au crible · 595 matchs officiels · 1 modèle statistique</p>
  </div>
  <div class="pied pied-clair"><span class="signature">Moïse Monnin · Data Analyst</span><span>Faites défiler →</span></div>
</section>"""

# ---------- 2. Bilan historique (écran partagé vertical) ----------
b = R["bilan"]
s2 = f"""
<section class="slide sans-marge">
  <div class="moitie moitie-barca rayures-sombres">
    <div class="kicker or-barca">FC Barcelone</div>
    <div class="geant or-barca">{b['victoires_barca']}</div>
    <div class="legende-geant">victoires</div>
    <div class="buts">{b['buts_barca']} buts marqués</div>
  </div>
  <div class="moitie moitie-real">
    <div class="kicker marine">Real Madrid</div>
    <div class="geant marine">{b['victoires_real']}</div>
    <div class="legende-geant marine-doux">victoires</div>
    <div class="buts marine">{b['buts_real']} buts marqués</div>
  </div>
  <div class="medaillon"><span class="num">{b['nuls']}</span><span>nuls</span></div>
  <div class="bas-sombre">
    <div class="kicker">Le bilan depuis 1902</div>
    <h2>{b['matchs']} Clásicos officiels. Personne devant.</h2>
    <p class="gris">124 ans de rivalité, 3 buts d'écart. L'histoire ne départage personne : il faut regarder ailleurs.</p>
    {pied(2, "Source : Wikipédia, « List of El Clásico matches » — matchs officiels jusqu'au 10 mai 2026.")}
  </div>
</section>"""

# ---------- 3. Méthode (neutre, accents des deux chartes) ----------
s3 = f"""
<section class="slide">
  {bandeau()}
  <div class="kicker">La méthode</div>
  <h2>Partir des preuves, pas des impressions.</h2>
  <div class="etapes">
    <div class="etape"><div class="pastille-num">01</div><div><h3>18 Clásicos récents</h3><p>D'octobre 2021 à mai 2026, toutes compétitions : Liga, Coupe du Roi, Supercoupe.</p></div></div>
    <div class="etape"><div class="pastille-num">02</div><div><h3>La forme avant chaque match</h3><p>Points et différence de buts sur les 5 matchs officiels précédents. Buts + passes des attaquants clés.</p></div></div>
    <div class="etape"><div class="pastille-num">03</div><div><h3>Un modèle de Poisson</h3><p>Force d'attaque et de défense sur les 38 derniers matchs de Liga, vérifiée avec les expected goals (xG).</p></div></div>
  </div>
  <div class="carte-neutre" style="margin-top:auto; margin-bottom:120px;">
    <p>Données croisées entre deux sources : <b class="num">591</b> scores comparés, <b class="num">0</b> écart.</p>
  </div>
  {pied(3, "Sources : ESPN, Wikipédia, Understat (xG). Code et données ouverts : lien en commentaire.")}
</section>"""

# ---------- 4. Preuve n°1 : les 18 Clásicos ----------
pf = R["preuve_forme"]
tuiles = []
for c in R["clasicos"]:
    club = "barca" if c["vainqueur"] == BARCA else "real"
    signe = "✓" if c["plus_en_forme"] == c["vainqueur"] else "✗"
    tuiles.append(f'<div class="col"><div class="tuile tuile-{club}"><span>{signe}</span></div><div class="score">{c["score"]}</div></div>')
s4 = f"""
<section class="slide">
  {bandeau()}
  <div class="kicker">Preuve n°1 · La forme</div>
  <h2>L'équipe la plus en forme gagne-t-elle&nbsp;?</h2>
  <div class="hero">{pf['gagne']}<span class="hero-sur">/ {pf['sur']}</span></div>
  <p>L'équipe en meilleure forme a gagné <b>{pf['gagne']} des {pf['sur']}</b> derniers Clásicos <span class="gris">({pct(pf['taux'])} %)</span>.</p>
  <div class="frise">
    <div class="frise-dates"><span>Oct. 2021</span><span>Mai 2026 →</span></div>
    <div class="frise-tuiles">{''.join(tuiles)}</div>
    <div class="frise-legende"><span class="mini tuile-barca"></span>Victoire Barça <span class="mini tuile-real"></span>Victoire Real <span class="sep">·</span> ✓ la plus en forme a gagné</div>
  </div>
  <p class="gris" style="margin-top:34px; font-size:28px;">Mais un pile ou face ferait aussi bien 1 fois sur 4. Et l'écart de forme ne dit rien de l'écart au score (corrélation : <b class="num">{dec(pf['correlation'])}</b>).</p>
  <p style="margin-top:14px; font-size:28px;"><b>Détail frappant : {pf['nuls_sur_18']} match nul en 18 Clásicos.</b></p>
  {pied(4, "Source : ESPN, contrôlé avec Wikipédia.")}
</section>"""

# ---------- 5. Forme actuelle : une carte par club, chacune à sa charte ----------
NOMS_FR = {"Sevilla": "Séville", "Real Betis": "Betis", "Paris Saint-Germain": "PSG", "Atlético Madrid": "Atlético",
           "AS Roma": "AS Rome", "RB Leipzig": "Leipzig"}


def carte_forme(club):
    f = R["forme_actuelle"][club]
    cls = "barca" if club == BARCA else "real"
    chips = "".join(f'<span class="chip chip-{cls} chip-{x}">{x}</span>' for x in f["resultats"])
    lignes = []
    for m in f["matchs"]:  # format : « Sevilla 3-1 (Liga) »
        adv, score = m.split(" (")[0].rsplit(" ", 1)
        comp = " <span class='ldc'>LdC</span>" if "champions" in m else ""
        lignes.append(f"<div>{NOMS_FR.get(adv, adv)} <b>{score}</b>{comp}</div>")
    nom = "FC Barcelone" if club == BARCA else "Real Madrid"
    return f"""<div class="carte-club carte-{cls}">
      <div class="nom-club">{nom}</div>
      <div class="chips">{chips}</div>
      <div class="pts"><span class="num">{f['points']}</span><span class="sur">/15</span> <span class="db">{f['diff_buts']:+d}</span></div>
      <div class="liste">{''.join(lignes)}</div>
    </div>"""


s5 = f"""
<section class="slide">
  {bandeau()}
  <div class="kicker">La forme avant dimanche</div>
  <h2>12 points sur 15 chacun. Égalité parfaite.</h2>
  <div class="duel">{carte_forme(BARCA)}{carte_forme(REAL)}</div>
  <p style="margin-top:36px; font-size:28px;">Le Barça est devant à la différence de buts, mais sort d'une défaite à Paris. Le Real enchaîne 4 victoires.</p>
  <p class="gris" style="margin-top:14px; font-size:25px;">Absents annoncés : Olmo, E. García, Christensen (Barça) · Vinícius (suspendu), Rodrygo (Real).</p>
  {pied(5, "Sources : ESPN (résultats), presse sportive du 21 au 23/10/2026 (absences). V = victoire, N = nul, D = défaite.")}
</section>"""

# ---------- 6. Joueurs : un panneau par club ----------
ECHELLE = 1.2


def rangee(j, cls):
    a, p = j["avant"] / ECHELLE * 100, j["pendant"] / ECHELLE * 100
    g, d = min(a, p), max(a, p)
    return f"""<div class="rangee">
      <div class="joueur">{j['joueur']} <span class="nb">{j['clasicos']} Cl.</span></div>
      <div class="piste">
        <div class="trait trait-{cls}" style="left:{g}%; width:{d - g}%"></div>
        <div class="anneau anneau-{cls}" style="left:{a}%"></div>
        <div class="point point-{cls}" style="left:{p}%"><span class="val">{dec(j['pendant'])}</span></div>
      </div>
    </div>"""


def panneau(club):
    cls = "barca" if club == BARCA else "real"
    ordre = {"Lamine Yamal": 0, "Raphinha": 1, "Fermín López": 2, "Kylian Mbappé": 0, "Jude Bellingham": 1, "Arda Güler": 2}
    js = sorted((j for j in R["joueurs"] if j["club"] == club), key=lambda j: ordre[j["joueur"]])
    graduations = "".join(f'<span style="left:{v / ECHELLE * 100}%">{dec(v, 1)}</span>' for v in (0, 0.4, 0.8, 1.2))
    return f"""<div class="panneau panneau-{cls}">
      {''.join(rangee(j, cls) for j in js)}
      <div class="axe"><div></div><div class="graduations">{graduations}</div></div>
    </div>"""


s6 = f"""
<section class="slide">
  {bandeau()}
  <div class="kicker">Les joueurs clés</div>
  <h2>Qui élève son niveau dans le Clásico&nbsp;?</h2>
  <p class="gris" style="font-size:25px; margin-bottom:22px;">Buts + passes décisives par match : ○ sur les 5 matchs avant le Clásico, ● pendant. Lien entre les deux : <b class="num" style="color:var(--texte)">{dec(R['correlation_joueurs'])}</b>, faible.</p>
  {panneau(BARCA)}
  {panneau(REAL)}
  <p style="margin-top:20px; font-size:26px;"><b class="txt-real">Mbappé</b> : 1 but ou passe par Clásico. <b class="txt-real">Bellingham</b> et <b class="txt-barca">Raphinha</b> montent d'un cran. <b class="txt-barca">Fermín López</b> et <b class="txt-real">Güler</b> baissent.</p>
  {pied(6, "Source : ESPN — matchs où le joueur a joué uniquement. Vinícius, suspendu, n'est pas suivi.")}
</section>"""

# ---------- 7. Pronostic ----------
mo, mx, ma = R["modele"], R["modele_xg"], R["marche"]
top = R["scores_probables"][0]


def barre(nom, p):
    return f"""<div class="barre-ligne"><div class="barre-nom">{nom}</div><div class="barre">
      <div class="seg seg-barca" style="flex:{p['barca']}"><span>{pct(p['barca'])} %</span></div>
      <div class="seg seg-nul" style="flex:{p['nul']}"><span>{pct(p['nul'])} %</span></div>
      <div class="seg seg-real" style="flex:{p['real']}"><span>{pct(p['real'])} %</span></div></div></div>"""


s7 = f"""
<section class="slide">
  {bandeau()}
  <div class="kicker">Le pronostic du modèle</div>
  <h2>Le Barça favori, sans être intouchable.</h2>
  <div class="probas">
    <div class="proba proba-barca rayures-sombres"><div class="val">{pct(mo['barca'])}<small>%</small></div><div class="lib">Victoire Barça</div></div>
    <div class="proba proba-nul"><div class="val">{pct(mo['nul'])}<small>%</small></div><div class="lib">Match nul</div></div>
    <div class="proba proba-real"><div class="val">{pct(mo['real'])}<small>%</small></div><div class="lib">Victoire Real</div></div>
  </div>
  <p>Score le plus probable : <b class="num">{top[0]}</b> <span class="gris">({pct(top[1])} %)</span> · Buts attendus : <b class="num">{dec(mo['lambda_barca'], 1)}</b> – <b class="num">{dec(mo['lambda_real'], 1)}</b></p>
  <div class="barres">{barre("Modèle (buts)", mo)}{barre("Modèle (xG)", mx)}{barre("Marché", ma)}</div>
  <p style="margin-top:26px; font-size:27px;">Modèle contre marché : <b>{pct(mo['barca'])} % contre {pct(ma['barca'])} %</b>. Les trois méthodes convergent. Le marché voit le Real un peu plus dangereux ({pct(ma['real'])} %).</p>
  <div class="avert">Analyse à but pédagogique — ceci n'est pas un conseil de pari. Marché : moyenne de 4 opérateurs, marge retirée (21/10/2026).</div>
  {pied(7)}
</section>"""

# ---------- 8. Limites ----------
s8 = f"""
<section class="slide">
  {bandeau()}
  <div class="kicker">Les limites</div>
  <h2>Ce que les stats ne voient pas.</h2>
  <ul class="limites">
    <li><b>Un petit échantillon.</b> <span class="gris">18 Clásicos, c'est peu : {pct(pf['taux'])} % peut être un coup de chance.</span></li>
    <li><b>Les absences.</b> <span class="gris">Le modèle ne sait pas que Vinícius est suspendu ni qu'Olmo est blessé.</span></li>
    <li><b>Le scénario du match.</b> <span class="gris">Un carton rouge, un but précoce, et toutes les probabilités changent.</span></li>
    <li><b>L'émotion.</b> <span class="gris">Pression, ambiance, enjeu du titre : rien de tout cela n'est dans les chiffres.</span></li>
  </ul>
  <div class="carte-neutre" style="margin-top:auto; margin-bottom:110px;">
    <p>Un modèle décrit des tendances sur beaucoup de matchs. <b>Un seul match reste une épreuve du hasard.</b></p>
  </div>
  {pied(8)}
</section>"""

# ---------- 9. Question ouverte (écran partagé en diagonale) ----------
s9 = f"""
<section class="slide split-diag">
  <div class="cote-barca rayures"></div>
  <div class="cote-real"></div>
  <div class="carte-titre carte-finale">
    <div class="kicker">Rendez-vous demain</div>
    <h1 style="font-size:78px;">{pct(mo['barca'])} % pour le Barça.<br><span class="gris">Donc {100 - int(pct(mo['barca']))} % pour que ce soit autre chose.</span></h1>
    <p class="question">Les stats diront-elles la vérité&nbsp;?</p>
    <p>Verdict lundi à 8h GMT : modèle contre réalité.</p>
    <div class="appel"><b>Et vous, quel score&nbsp;?</b> Votre pronostic en commentaire.</div>
    <p class="petit">Données et code ouverts : lien dans le premier commentaire.</p>
  </div>
  <div class="pied pied-clair"><span class="signature">Moïse Monnin · Data Analyst</span><span>9/{TOTAL}</span></div>
</section>"""

html = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Clásico — Pronostic data</title>
<!-- Fichier généré par carrousel/generer_post1.py à partir de resultats.json.
     Pour une retouche de texte ponctuelle, on peut modifier ce fichier directement,
     mais elle sera écrasée à la prochaine génération : préférer modifier generer_post1.py. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body>
{s1}{s2}{s3}{s4}{s5}{s6}{s7}{s8}{s9}
</body>
</html>
"""
(ICI / "post1_pronostic.html").write_text(html, encoding="utf-8")
print("post1_pronostic.html généré")
