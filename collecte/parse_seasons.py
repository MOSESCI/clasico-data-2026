"""Extrait les matchs officiels des pages saison Wikipédia (Barça & Real) vers un CSV."""
import csv, re, sys, glob, os
from datetime import datetime

raw, out = sys.argv[1], sys.argv[2]
BOX = re.compile(r"\{\{\s*football\s*box(?:\s*collapsible)?|\{\{\s*footballbox(?:\s*collapsible)?", re.I)
HEAD = re.compile(r"^(={2,5})\s*(.+?)\s*\1\s*$", re.M)

def clean_link(s):
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"\{\{[^{}]*\}\}", "", s)
    return re.sub(r"<[^>]+>.*?</[^>]+>|<[^>]+/>", "", s).strip()

def extract_block(t, i):
    depth, j = 0, i
    while j < len(t):
        if t.startswith("{{", j): depth += 1; j += 2; continue
        if t.startswith("}}", j):
            depth -= 1; j += 2
            if depth == 0: return t[i:j]
            continue
        j += 1
    return t[i:]

def fields(block):
    body = block[2:-2]
    parts, depth, cur = [], 0, ""
    k = 0
    while k < len(body):
        c2 = body[k:k+2]
        if c2 in ("{{", "[["): depth += 1; cur += c2; k += 2; continue
        if c2 in ("}}", "]]"): depth -= 1; cur += c2; k += 2; continue
        if body[k] == "|" and depth == 0: parts.append(cur); cur = ""; k += 1; continue
        cur += body[k]; k += 1
    parts.append(cur)
    d = {}
    for p in parts[1:]:
        if "=" in p:
            key, v = p.split("=", 1); d[key.strip().lower()] = v.strip()
    return d

def scorers(txt):
    """Liste (joueur, buts) hors buts contre son camp."""
    res = []
    for line in re.split(r"\n|<br\s*/?>|,(?![^{]*\}\})", txt):
        m = re.search(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", line)
        goals = re.findall(r"\{\{\s*goal\s*\|([^{}]*)\}\}", line, re.I)
        if not m or not goals: continue
        n = 0
        for g in goals:
            args = [a.strip() for a in g.split("|")]
            mins = [a for a in args if a and re.match(r"^\d+(\+\d+)?$", a)]
            ogs = [a for a in args if a.lower() in ("o.g.", "og")]
            n += max(len(mins) - len(ogs), 0) if ogs else len(mins)
        if re.search(r"\{\{\s*own goal|o\.g\.", line, re.I) and not re.search(r"pen", line): 
            continue
        if n: res.append((m.group(1).strip(), n))
    return res

def comp_of(heading_stack, url):
    h = " ".join(heading_stack).lower()
    u = (url or "").lower()
    if "friendl" in h or "pre-season" in h or "exhibition" in h: return None
    if "supercopa" in h or "super cup" in h and "uefa" not in h: return "Supercopa"
    if "uefa super cup" in h: return "UEFA Super Cup"
    if "copa del rey" in h: return "Copa del Rey"
    if "champions league" in h: return "Ligue des champions"
    if "europa league" in h: return "Ligue Europa"
    if "conference league" in h: return "Ligue Europa Conférence"
    if "club world cup" in h or "intercontinental" in h: return "Mondial des clubs"
    if "la liga" in h or "laliga" in h or "league" in h and "champions" not in h: return "Liga"
    return None

rows = []
for fn in sorted(glob.glob(os.path.join(raw, "20*_season.txt"))):
    club = "Barcelona" if "Barcelona" in fn else "Real Madrid"
    t = open(fn, encoding="utf-8").read()
    heads = [(m.start(), len(m.group(1)), clean_link(m.group(2))) for m in HEAD.finditer(t)]
    for m in BOX.finditer(t):
        stack = {}
        for pos, lvl, name in heads:
            if pos > m.start(): break
            stack[lvl] = name
            for l in list(stack):
                if l > lvl: del stack[l]
        hs = [stack[l] for l in sorted(stack)]
        d = fields(extract_block(t, m.start()))
        comp = comp_of(hs, d.get("report"))
        if comp is None: continue
        date = clean_link(d.get("date", ""))
        dm = re.search(r"(\d{1,2} \w+ \d{4})", date)
        if not dm: continue
        dt = datetime.strptime(dm.group(1), "%d %B %Y").date()
        score = clean_link(d.get("score", ""))
        sm = re.search(r"(\d+)\s*[–-]\s*(\d+)", score)
        if not sm: continue  # match pas encore joué
        t1, t2 = clean_link(d.get("team1", "")), clean_link(d.get("team2", ""))
        home = club in t1 or (club == "Real Madrid" and "Madrid" in t1 and "Atlético" not in t1)
        g1, g2 = int(sm.group(1)), int(sm.group(2))
        gf, ga = (g1, g2) if home else (g2, g1)
        opp = t2 if home else t1
        mine = d.get("goals1" if home else "goals2", "")
        rows.append({"club": club, "date": dt.isoformat(), "competition": comp,
                     "round": clean_link(d.get("round", "")), "adversaire": opp,
                     "domicile": int(home), "buts_pour": gf, "buts_contre": ga,
                     "score_brut": score, "buteurs": "; ".join(f"{p}:{n}" for p, n in scorers(mine)),
                     "source": "Wikipedia — " + os.path.basename(fn).replace("_", " ").replace(".txt", "")})

rows.sort(key=lambda r: (r["club"], r["date"]))
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), Counter((r["club"], r["competition"]) for r in rows))
