"""Construit video/scene.html : les 8 scènes animées du Reel (1080 × 1920), pilotées image par image.

L'animation n'utilise pas d'horloge : la fonction JavaScript render(t) dessine l'état exact à l'instant t.
C'est ce qui permet de capturer chaque image sans saccade (voir rendre_video.py).
Usage : python video/generer_scene.py
"""
import json
from pathlib import Path
from minutage import T, DUREE

ICI = Path(__file__).parent
R = json.loads((ICI.parent / "resultats.json").read_text(encoding="utf-8"))
J = {j["joueur"]: j for j in R["joueurs"]}
DONNEES = {
    "bilan": R["bilan"],
    "clasicos": [{"score": c["score"], "barca": c["vainqueur"] == "Barcelona", "ok": c["plus_en_forme"] == c["vainqueur"]}
                 for c in R["clasicos"]],
    "preuve": R["preuve_forme"],
    "forme": {k: {"r": v["resultats"], "pts": v["points"], "db": v["diff_buts"]} for k, v in R["forme_actuelle"].items()},
    "joueurs": [{"nom": n, "club": "barca" if J[n]["club"] == "Barcelona" else "real", "avant": J[n]["avant"], "pendant": J[n]["pendant"]}
                for n in ("Raphinha", "Kylian Mbappé", "Jude Bellingham")],
    "modele": R["modele"], "marche": R["marche"], "score": R["scores_probables"][0][0],
}

HTML = r"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>Clásico — Reel</title>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Inter:wght@500;600;700&display=swap" rel="stylesheet">
<style>
:root { --nuit:#0D1326; --nuit2:#151C35; --texte:#F5F3EE; --gris:#A3A9BD;
  --bleu:#004D98; --grenat:#A50044; --or:#EDBB00; --blanc:#FFFFFF; --rmor:#FEBE10; --marine:#00529F; --encre:#0B1F3F; --creme:#FBF6E6; }
* { margin:0; padding:0; box-sizing:border-box; }
html,body { width:1080px; height:1920px; overflow:hidden; background:var(--nuit); color:var(--texte); font-family:Inter,sans-serif; }
#scene { position:relative; width:1080px; height:1920px; overflow:hidden;
  background: radial-gradient(120% 70% at 50% 0%, var(--nuit2) 0%, var(--nuit) 70%); }
.s { position:absolute; inset:0; display:none; }
.abs { position:absolute; }
.rayures { background: repeating-linear-gradient(90deg, var(--bleu) 0 90px, var(--grenat) 90px 180px); }
.rayures-s { background: linear-gradient(180deg, rgba(6,18,48,.5), rgba(6,18,48,.85)), repeating-linear-gradient(90deg, var(--bleu) 0 90px, var(--grenat) 90px 180px); }
.blancrm { background: linear-gradient(200deg, var(--blanc) 55%, var(--creme)); }
.cond { font-family:"Barlow Condensed"; font-weight:800; text-transform:uppercase; line-height:.95; }
.kicker { font:700 30px Inter; letter-spacing:.18em; text-transform:uppercase; color:var(--gris); }
.centre { left:0; right:0; text-align:center; }
.bandeau { position:absolute; top:0; left:0; right:0; height:22px; display:flex; z-index:20; }
.bandeau i { flex:1; } .bandeau i:first-child { background: repeating-linear-gradient(90deg, var(--bleu) 0 44px, var(--grenat) 44px 88px); }
.bandeau i:last-child { background:var(--blanc); border-bottom:7px solid var(--rmor); }
#progres { position:absolute; top:22px; left:0; height:8px; z-index:21; background: linear-gradient(90deg, var(--bleu), var(--grenat), var(--rmor)); }
#signature { position:absolute; top:52px; left:50%; transform:translateX(-50%); white-space:nowrap; padding:12px 26px; border-radius:40px; background:rgba(13,19,38,.88); font:700 26px Inter; letter-spacing:.08em; color:var(--texte); z-index:21; }
#volet { position:absolute; top:-200px; width:1700px; height:2400px; z-index:50; display:none;
  background: linear-gradient(90deg, var(--bleu) 0 18%, var(--grenat) 18% 36%, var(--or) 36% 42%, var(--blanc) 42% 82%, var(--rmor) 82% 100%);
  transform-origin:center; }
/* scène 1 et 8 */
.diag-b { clip-path: polygon(0 0, 70% 0, 30% 100%, 0 100%); }
.diag-r { clip-path: polygon(70% 0, 100% 0, 100% 100%, 30% 100%); }
.diag-or { background:var(--rmor); clip-path: polygon(69.3% 0, 70.7% 0, 30.7% 100%, 29.3% 100%); }
.vs { width:230px; height:230px; border-radius:50%; background:var(--nuit); border:8px solid var(--rmor);
  display:grid; place-items:center; font:800 100px "Barlow Condensed"; left:425px; top:560px; }
.carte { left:56px; right:56px; background:rgba(13,19,38,.95); border-radius:36px; padding:70px 60px 60px; overflow:hidden; box-shadow:0 40px 90px rgba(0,0,0,.5); }
.carte::before { content:""; position:absolute; top:0; left:0; right:0; height:14px;
  background: linear-gradient(90deg, var(--bleu) 0 25%, var(--grenat) 25% 50%, var(--blanc) 50% 75%, var(--rmor) 75%); }
/* scène 3 */
.tuile { width:140px; height:190px; border-radius:14px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; }
.tuile b { font:800 66px Inter; line-height:1; }
.tuile span { font:800 34px "Barlow Condensed"; }
.t-barca { background: repeating-linear-gradient(90deg, var(--bleu) 0 12px, var(--grenat) 12px 24px); color:var(--or); }
.t-barca span { color:var(--texte); }
.t-real { background:var(--blanc); color:var(--marine); box-shadow: inset 0 -12px 0 var(--rmor); }
/* scène 5 */
.club { left:60px; right:60px; height:420px; border-radius:30px; padding:40px 46px; }
.chip { display:inline-grid; place-items:center; width:104px; height:104px; border-radius:18px; font:800 58px "Barlow Condensed"; margin-right:14px; }
/* scène 6 */
.panneau { left:60px; right:60px; border-radius:30px; padding:20px 40px; }
.rangee { position:relative; height:210px; }
.rangee .nom { position:absolute; left:0; top:22px; font:800 54px "Barlow Condensed"; text-transform:uppercase; }
.piste { position:absolute; left:0; right:0; top:120px; height:6px; border-radius:3px; }
.anneau, .point { position:absolute; top:123px; border-radius:50%; transform:translate(-50%,-50%); }
.anneau { width:46px; height:46px; border:7px solid; }
.point { width:52px; height:52px; }
.valeur { position:absolute; top:152px; font:800 52px "Barlow Condensed"; transform:translateX(-50%); }
/* scène 7 */
.barre-l { left:80px; right:80px; height:150px; }
.barre-l .lib { font:700 32px "Barlow Condensed"; text-transform:uppercase; letter-spacing:.1em; color:var(--gris); margin-bottom:10px; }
.barre-l .fond { position:relative; height:100px; border-radius:14px; background:rgba(255,255,255,.06); overflow:hidden; }
.barre-l .rempli { position:absolute; left:0; top:0; bottom:0; border-radius:14px; }
.barre-l .pct { position:absolute; top:6px; font:800 86px "Barlow Condensed"; }
</style></head>
<body><div id="scene">
  <div class="bandeau"><i></i><i></i></div><div id="progres"></div>
  <div id="signature">MOÏSE MONNIN · DATA ANALYST</div>

  <!-- 1 · Accroche -->
  <div class="s" id="s1">
    <div class="abs rayures diag-b" id="s1b" style="inset:0"></div>
    <div class="abs blancrm diag-r" id="s1r" style="inset:0"></div>
    <div class="abs diag-or" id="s1o" style="inset:0"></div>
    <div class="abs cond" id="s1lb" style="left:70px; top:150px; font-size:64px; color:var(--or)">FC Barcelone</div>
    <div class="abs cond" id="s1lr" style="right:70px; top:150px; font-size:64px; color:var(--marine)">Real Madrid</div>
    <div class="abs vs" id="s1vs">VS</div>
    <div class="abs carte" id="s1c" style="top:1000px">
      <div class="kicker" id="s1k">Clásico · 25.10 · 20h00 GMT</div>
      <div class="cond" id="s1t" style="font-size:138px; margin-top:28px">Les données ont-elles déjà le résultat&nbsp;?</div>
    </div>
  </div>

  <!-- 2 · Bilan -->
  <div class="s" id="s2">
    <div class="abs rayures-s" id="s2b" style="left:0; top:0; width:540px; height:1220px"></div>
    <div class="abs blancrm" id="s2r" style="right:0; top:0; width:540px; height:1220px; border-left:10px solid var(--rmor)"></div>
    <div class="abs cond" style="left:0; width:540px; top:200px; text-align:center; font-size:56px; color:var(--or)">FC Barcelone</div>
    <div class="abs cond" style="right:0; width:540px; top:200px; text-align:center; font-size:56px; color:var(--marine)">Real Madrid</div>
    <div class="abs cond" id="s2nb" style="left:0; width:540px; top:330px; text-align:center; font-size:330px; color:var(--or)">0</div>
    <div class="abs cond" id="s2nr" style="right:0; width:540px; top:330px; text-align:center; font-size:330px; color:var(--marine)">0</div>
    <div class="abs cond" style="left:0; width:540px; top:660px; text-align:center; font-size:56px; letter-spacing:.12em">Victoires</div>
    <div class="abs cond" style="right:0; width:540px; top:660px; text-align:center; font-size:56px; letter-spacing:.12em; color:var(--encre)">Victoires</div>
    <div class="abs" id="s2m" style="left:405px; top:840px; width:270px; height:270px; border-radius:50%; background:var(--nuit); border:9px solid var(--rmor); display:flex; flex-direction:column; align-items:center; justify-content:center">
      <div class="cond" style="font-size:130px">__NULS__</div><div class="cond" style="font-size:40px; color:var(--gris); letter-spacing:.14em">nuls</div></div>
    <div class="abs centre" id="s2t" style="top:1290px; padding:0 70px">
      <div class="kicker">Le bilan depuis 1902</div>
      <div class="cond" style="font-size:120px; margin-top:24px">__MATCHS__ Clásicos.<br>Personne devant.</div>
    </div>
  </div>

  <!-- 3 · Preuve n°1 -->
  <div class="s" id="s3">
    <div class="abs" style="left:80px; right:80px; top:170px">
      <div class="kicker">Preuve n°1 · la forme</div>
      <div class="cond" style="font-size:104px; margin-top:22px">L'équipe la plus en forme gagne-t-elle&nbsp;?</div>
    </div>
    <div class="abs" id="s3g" style="left:80px; top:560px; width:920px; height:620px"></div>
    <div class="abs centre cond" id="s3h" style="top:1250px; font-size:300px">0<span style="font-size:150px; color:var(--gris)"> / 18</span></div>
    <div class="abs centre" id="s3c" style="top:1560px; font:600 40px Inter; color:var(--gris)">✓ = l'équipe la plus en forme a gagné</div>
  </div>

  <!-- 4 · Zéro nul -->
  <div class="s" id="s4">
    <div class="abs" id="s4f" style="inset:0; background:radial-gradient(60% 40% at 50% 42%, rgba(254,190,16,.55), transparent 70%)"></div>
    <div class="abs centre cond" id="s4z" style="top:330px; font-size:760px; line-height:.85">0</div>
    <div class="abs centre cond" id="s4a" style="top:1060px; font-size:170px">Match nul</div>
    <div class="abs centre" id="s4b" style="top:1270px; font:700 54px Inter; color:var(--gris)">en 18 Clásicos depuis 2021</div>
  </div>

  <!-- 5 · Forme -->
  <div class="s" id="s5">
    <div class="abs" style="left:60px; right:60px; top:170px">
      <div class="kicker">La forme avant dimanche</div>
      <div class="cond" style="font-size:110px; margin-top:22px">5 derniers matchs</div>
    </div>
    <div class="abs club rayures-s" id="s5b" style="top:470px; border-bottom:14px solid var(--or)">
      <div class="cond" style="font-size:64px; color:var(--or)">FC Barcelone</div>
      <div id="s5bc" style="margin-top:36px"></div>
      <div class="cond" style="font-size:96px; margin-top:34px"><span id="s5bp">0</span><span style="font-size:56px; opacity:.7">/15</span> <span style="color:var(--or)">__DBB__</span></div>
    </div>
    <div class="abs club blancrm" id="s5r" style="top:940px; color:var(--encre); border-bottom:14px solid var(--rmor)">
      <div class="cond" style="font-size:64px; color:var(--marine)">Real Madrid</div>
      <div id="s5rc" style="margin-top:36px"></div>
      <div class="cond" style="font-size:96px; margin-top:34px"><span id="s5rp">0</span><span style="font-size:56px; opacity:.7">/15</span> <span style="color:var(--marine)">__DBR__</span></div>
    </div>
    <div class="abs centre cond" id="s5e" style="top:1440px; font-size:120px; color:var(--rmor)">Égalité parfaite.</div>
  </div>

  <!-- 6 · Joueurs -->
  <div class="s" id="s6">
    <div class="abs" style="left:60px; right:60px; top:170px">
      <div class="kicker">Les joueurs clés</div>
      <div class="cond" style="font-size:104px; margin-top:22px">Qui élève son niveau dans le Clásico&nbsp;?</div>
    </div>
    <div class="abs panneau rayures-s" id="s6b" style="top:560px; height:250px"></div>
    <div class="abs panneau blancrm" id="s6r" style="top:840px; height:460px; color:var(--encre)"></div>
    <div class="abs centre" id="s6l" style="top:1350px; font:600 38px Inter; color:var(--gris)">Buts + passes décisives par match<br>○ 5 matchs avant · ● pendant le Clásico</div>
  </div>

  <!-- 7 · Pronostic -->
  <div class="s" id="s7">
    <div class="abs" style="left:80px; right:80px; top:170px">
      <div class="kicker">Le pronostic du modèle</div>
      <div class="cond" style="font-size:110px; margin-top:22px">Dimanche, 20h GMT</div>
    </div>
    <div class="abs barre-l" style="top:480px"><div class="lib">Victoire Barça</div><div class="fond"><div class="rempli rayures" id="s7b1"></div><div class="pct" id="s7p1" style="color:var(--or)"></div></div></div>
    <div class="abs barre-l" style="top:680px"><div class="lib">Match nul</div><div class="fond"><div class="rempli" id="s7b2" style="background:#3A4160"></div><div class="pct" id="s7p2"></div></div></div>
    <div class="abs barre-l" style="top:880px"><div class="lib">Victoire Real</div><div class="fond"><div class="rempli" id="s7b3" style="background:var(--blanc); box-shadow:inset 0 -10px 0 var(--rmor)"></div><div class="pct" id="s7p3" style="color:var(--blanc)"></div></div></div>
    <div class="abs carte" id="s7s" style="top:1130px; text-align:center; padding:60px 40px 50px">
      <div class="kicker">Score le plus probable</div>
      <div class="cond" style="font-size:200px; margin-top:16px">__SCORE__</div>
      <div id="s7m" style="font:600 36px Inter; color:var(--gris); margin-top:14px">Le marché : Barça __MARCHE__ %</div>
    </div>
    <div class="abs centre" style="top:1770px; font:600 26px Inter; color:var(--gris)">Analyse pédagogique — pas un conseil de pari</div>
  </div>

  <!-- 8 · Question ouverte -->
  <div class="s" id="s8">
    <div class="abs rayures diag-b" id="s8b" style="inset:0"></div>
    <div class="abs blancrm diag-r" id="s8r" style="inset:0"></div>
    <div class="abs diag-or" id="s8o" style="inset:0"></div>
    <div class="abs carte" id="s8c" style="top:420px">
      <div class="kicker">Rendez-vous lundi</div>
      <div class="cond" style="font-size:128px; margin-top:26px">Les stats diront-elles la vérité&nbsp;?</div>
      <div id="s8a" class="cond" style="font-size:68px; margin-top:46px; color:var(--rmor)">Ton score en commentaire 👇</div>
      <div style="font:600 34px Inter; color:var(--gris); margin-top:40px">Analyse complète, données et code : lien en bio</div>
      <div style="font:700 34px Inter; margin-top:30px">Moïse Monnin · Data Analyst</div>
    </div>
  </div>

  <div id="volet"></div>
</div>
<script>
const T = __T__, D = __D__, DUREE = __DUREE__;
const $ = id => document.getElementById(id);
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const p = (t, a, b) => clamp((t - a) / (b - a));
const out3 = x => 1 - Math.pow(1 - x, 3);
const back = x => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const st = (el, o) => { el = typeof el === "string" ? $(el) : el; Object.assign(el.style, o); };
const fr = n => n.toFixed(2).replace(".", ",");

// Construction des éléments répétés (tuiles, pastilles, joueurs)
D.clasicos.forEach((c, i) => {
  const d = document.createElement("div");
  d.className = "abs tuile " + (c.barca ? "t-barca" : "t-real");
  d.id = "tuile" + i;
  d.style.left = (i % 6) * 156 + "px"; d.style.top = Math.floor(i / 6) * 210 + "px";
  d.innerHTML = `<b>${c.ok ? "✓" : "✗"}</b><span>${c.score}</span>`;
  $("s3g").appendChild(d);
});
for (const [club, id] of [["Barcelona", "s5bc"], ["Real Madrid", "s5rc"]]) {
  [...D.forme[club].r].forEach((r, i) => {
    const s = document.createElement("span");
    s.className = "chip"; s.id = id + i; s.textContent = r;
    const barca = club === "Barcelona";
    Object.assign(s.style, r === "V"
      ? { background: barca ? "var(--or)" : "var(--marine)", color: barca ? "#061A3A" : "#fff" }
      : { border: "5px solid " + (barca ? "var(--texte)" : "var(--encre)"), color: barca ? "var(--texte)" : "var(--encre)" });
    $(id).appendChild(s);
  });
}
const PISTE = 820, ECH = 1.2;
D.joueurs.forEach((j, i) => {
  const parent = j.club === "barca" ? $("s6b") : $("s6r");
  const coul = j.club === "barca" ? "var(--or)" : "var(--marine)";
  const r = document.createElement("div");
  r.className = "rangee";
  r.innerHTML = `<div class="nom">${j.nom}</div>
    <div class="piste" style="background:${j.club === "barca" ? "rgba(255,255,255,.25)" : "rgba(11,31,63,.18)"}"></div>
    <div class="anneau" id="an${i}" style="border-color:${coul}"></div>
    <div class="point" id="pt${i}" style="background:${j.club === "barca" ? "var(--or)" : "var(--rmor)"}; ${j.club === "real" ? "border:6px solid var(--marine)" : ""}"></div>
    <div class="valeur" id="va${i}" style="color:${j.club === "barca" ? "var(--or)" : "var(--marine)"}"></div>`;
  parent.appendChild(r);
});

function scene(t) { let k = 0; while (k < 7 && t >= T.scenes[k + 1]) k++; return k + 1; }

function render(t) {
  const n = scene(t);
  for (let k = 1; k <= 8; k++) $("s" + k).style.display = k === n ? "block" : "none";
  st("progres", { width: (t / DUREE * 100) + "%" });
  $("signature").style.opacity = (n === 1 || n === 8) ? 0 : 1;

  // Volet de transition centré sur chaque changement de scène
  let v = null;
  for (const b of T.scenes.slice(1, 8)) if (t > b - 0.22 && t < b + 0.22) v = p(t, b - 0.22, b + 0.22);
  if (v === null) st("volet", { display: "none" });
  else st("volet", { display: "block", transform: `translateX(${-1800 + v * 3300}px) skewX(-14deg)` });

  if (n === 1) {
    const e = out3(p(t, 0, 0.55));
    st("s1b", { transform: `translateX(${(e - 1) * 100}%)` });
    st("s1r", { transform: `translateX(${(1 - e) * 100}%)` });
    st("s1o", { opacity: p(t, 0.4, 0.6) });
    st("s1lb", { opacity: p(t, 0.45, 0.8), transform: `translateY(${(1 - out3(p(t, 0.45, 0.8))) * 40}px)` });
    st("s1lr", { opacity: p(t, 0.5, 0.85), transform: `translateY(${(1 - out3(p(t, 0.5, 0.85))) * 40}px)` });
    st("s1vs", { transform: `scale(${back(p(t, T.vs, T.vs + 0.4))})` });
    const c = out3(p(t, T.titre1, T.titre1 + 0.5));
    st("s1c", { opacity: c, transform: `translateY(${(1 - c) * 160}px)` });
    st("s1t", { opacity: p(t, T.titre1 + 0.2, T.titre1 + 0.6) });
  }
  if (n === 2) {
    const a = T.scenes[1], c = out3(p(t, T.compteurs[0], T.compteurs[1]));
    st("s2b", { transform: `translateY(${(1 - out3(p(t, a, a + 0.4))) * -100}%)` });
    st("s2r", { transform: `translateY(${(1 - out3(p(t, a, a + 0.4))) * 100}%)` });
    $("s2nb").textContent = Math.round(c * D.bilan.victoires_barca);
    $("s2nr").textContent = Math.round(c * D.bilan.victoires_real);
    st("s2m", { transform: `scale(${back(p(t, T.medaillon, T.medaillon + 0.4))})` });
    const l = out3(p(t, T.legende2, T.legende2 + 0.5));
    st("s2t", { opacity: l, transform: `translateY(${(1 - l) * 80}px)` });
  }
  if (n === 3) {
    D.clasicos.forEach((c, i) => {
      const d = p(t, T.tuiles + i * T.tuile_dt, T.tuiles + i * T.tuile_dt + T.tuile_duree);
      st("tuile" + i, { opacity: d > 0 ? 1 : 0, transform: `translateY(${(1 - back(d)) * -260}px)` });
    });
    const h = out3(p(t, T.hero3[0], T.hero3[1]));
    $("s3h").firstChild.textContent = Math.round(h * D.preuve.gagne);
    st("s3h", { opacity: p(t, T.hero3[0] - 0.1, T.hero3[0] + 0.15) });
    st("s3c", { opacity: p(t, T.hero3[1], T.hero3[1] + 0.3) });
  }
  if (n === 4) {
    const z = p(t, T.choc, T.impact), apres = t - T.impact;
    const tremble = apres > 0 && apres < 0.35 ? Math.sin(apres * 90) * 22 * (1 - apres / 0.35) : 0;
    st("s4z", { opacity: z > 0 ? 1 : 0, transform: `translate(${tremble}px, ${tremble * 0.6}px) scale(${3.2 - 2.2 * (z * z)})` });
    st("s4f", { opacity: apres > 0 ? Math.max(0, 1 - apres / 0.9) : 0 });
    st("s4a", { opacity: p(t, T.impact + 0.15, T.impact + 0.45), transform: `translateY(${(1 - out3(p(t, T.impact + 0.15, T.impact + 0.45))) * 60}px)` });
    st("s4b", { opacity: p(t, T.impact + 0.45, T.impact + 0.8) });
  }
  if (n === 5) {
    const b = out3(p(t, T.cartes5[0], T.cartes5[0] + 0.5)), r = out3(p(t, T.cartes5[1], T.cartes5[1] + 0.5));
    st("s5b", { transform: `translateX(${(1 - b) * -1100}px)` });
    st("s5r", { transform: `translateX(${(1 - r) * 1100}px)` });
    let pb = 0, pr = 0;
    for (const [club, id] of [["Barcelona", "s5bc"], ["Real Madrid", "s5rc"]]) {
      [...D.forme[club].r].forEach((x, i) => {
        const debut = T.pastilles5 + i * T.pastille_dt + (club === "Barcelona" ? 0 : 0.09);
        const k = p(t, debut, debut + 0.3);
        st(id + i, { transform: `scale(${back(k)})`, opacity: k > 0 ? 1 : 0 });
        if (t >= debut) { const v = x === "V" ? 3 : x === "N" ? 1 : 0; club === "Barcelona" ? pb += v : pr += v; }
      });
    }
    $("s5bp").textContent = pb; $("s5rp").textContent = pr;
    st("s5e", { transform: `scale(${back(p(t, T.egalite, T.egalite + 0.4))})` });
  }
  if (n === 6) {
    D.joueurs.forEach((j, i) => {
      const x = v => 30 + (v / ECH) * PISTE;
      const xa = x(j.avant), xp = x(j.pendant);
      const a = p(t, T.anneaux6 + i * 0.1, T.anneaux6 + i * 0.1 + 0.3);
      st("an" + i, { left: xa + "px", transform: `translate(-50%,-50%) scale(${back(a)})` });
      const k = out3(p(t, T.points6 + i * T.point_dt, T.points6 + i * T.point_dt + T.point_duree));
      const pos = xa + (xp - xa) * k, val = j.avant + (j.pendant - j.avant) * k;
      st("pt" + i, { left: pos + "px", opacity: a, transform: "translate(-50%,-50%)" });
      st("va" + i, { left: pos + "px", opacity: a });
      $("va" + i).textContent = fr(val);
    });
    st("s6l", { opacity: p(t, T.anneaux6, T.anneaux6 + 0.4) });
  }
  if (n === 7) {
    [["barca", 1], ["nul", 2], ["real", 3]].forEach(([k, i]) => {
      const debut = T.barres7 + (i - 1) * T.barre_dt, e = out3(p(t, debut, debut + T.barre_duree));
      const w = D.modele[k] * 920 * e;
      st("s7b" + i, { width: w + "px" });
      $("s7p" + i).textContent = Math.round(D.modele[k] * 100 * e) + " %";
      st("s7p" + i, { left: Math.max(w + 24, 24) + "px", opacity: e > 0 ? 1 : 0 });
    });
    const s = p(t, T.score7, T.score7 + 0.45);
    st("s7s", { opacity: s, transform: `scale(${0.6 + 0.4 * back(s)})` });
    st("s7m", { opacity: p(t, T.marche7, T.marche7 + 0.4) });
  }
  if (n === 8) {
    const a = T.scenes[7], e = out3(p(t, a, a + 0.5));
    st("s8b", { transform: `translateX(${(e - 1) * 100}%)` });
    st("s8r", { transform: `translateX(${(1 - e) * 100}%)` });
    st("s8o", { opacity: p(t, a + 0.35, a + 0.55) });
    const c = out3(p(t, a + 0.4, a + 0.9));
    st("s8c", { opacity: c, transform: `translateY(${(1 - c) * 160}px)` });
    const pulse = t > T.appel8 ? 1 + 0.06 * Math.sin((t - T.appel8) * 2 * Math.PI * 1.6) : 1;
    st("s8a", { opacity: p(t, T.appel8 - 0.3, T.appel8), transform: `scale(${pulse})`, transformOrigin: "left center" });
  }
}
window.render = render;
render(0);
</script></body></html>
"""

f = R["forme_actuelle"]
html = (HTML.replace("__T__", json.dumps(T)).replace("__D__", json.dumps(DONNEES, ensure_ascii=False))
        .replace("__DUREE__", str(DUREE)).replace("__NULS__", str(R["bilan"]["nuls"])).replace("__MATCHS__", str(R["bilan"]["matchs"]))
        .replace("__DBB__", f"{f['Barcelona']['diff_buts']:+d}").replace("__DBR__", f"{f['Real Madrid']['diff_buts']:+d}")
        .replace("__SCORE__", DONNEES["score"]).replace("__MARCHE__", str(round(R["marche"]["barca"] * 100))))
(ICI / "scene.html").write_text(html, encoding="utf-8")
print("scene.html généré")
