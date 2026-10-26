"""Compose la bande son du Reel : une musique originale (synthèse) + des effets calés sur l'animation.

Tout est généré par calcul : aucun échantillon externe, donc aucun problème de droits.
Usage : python video/audio.py [--projet verdict]                          (musique synthétisée)
        python video/audio.py [--projet verdict] --musique morceau.mp3    (remplace la musique, garde les effets)
"""
import subprocess, sys, wave
from pathlib import Path
import numpy as np
from projets import choisir

ARGS = sys.argv[1:]
NOM, CONF, MINUTAGE = choisir(ARGS)
T, DUREE = MINUTAGE.T, MINUTAGE.DUREE

ICI = Path(__file__).parent
SR = 44100
N = int(DUREE * SR)
rng = np.random.default_rng(7)
BPM, TEMPS = 120, 0.5  # un temps = 0,5 s


def piste():
    return np.zeros((N, 2))


def placer(buf, t, son, gain=1.0, pan=0.0):
    """Ajoute un son mono à l'instant t (secondes), pan de -1 (gauche) à 1 (droite)."""
    i = int(t * SR)
    if i >= N or i + len(son) <= 0:
        return
    s = son[: N - i] * gain
    buf[i:i + len(s), 0] += s * (1 - max(pan, 0))
    buf[i:i + len(s), 1] += s * (1 + min(pan, 0))


def env(n, attaque, chute):
    x = np.arange(n) / SR
    return np.minimum(1, x / max(attaque, 1e-4)) * np.exp(-x / chute)


def bruit_filtre(n, bas, haut):
    """Bruit blanc limité à une bande de fréquences (filtrage dans le domaine fréquentiel)."""
    spectre = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    spectre[(f < bas) | (f > haut)] = 0
    s = np.fft.irfft(spectre, n)
    return s / (np.abs(s).max() + 1e-9)


def note(freq, duree, harmoniques=6, decroissance=0.5):
    """Son « analogique » : somme d'harmoniques en 1/n (une scie adoucie)."""
    x = np.arange(int(duree * SR)) / SR
    s = sum(np.sin(2 * np.pi * freq * k * x) / k * decroissance ** (k - 1) for k in range(1, harmoniques + 1))
    return s / 1.6


# ---------------- Instruments ----------------
def kick():
    n = int(0.45 * SR); x = np.arange(n) / SR
    freq = 45 + 110 * np.exp(-x * 28)
    return np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-x * 7.5)


def clap():
    n = int(0.25 * SR)
    return bruit_filtre(n, 900, 6000) * env(n, 0.002, 0.07) * 0.8 + note(190, 0.25, 2) * env(n, 0.001, 0.05) * 0.4


def charleston(ouvert=False):
    n = int((0.18 if ouvert else 0.05) * SR)
    return bruit_filtre(n, 7000, 16000) * env(n, 0.001, 0.06 if ouvert else 0.015)


def basse(freq, duree):
    n = int(duree * SR)
    return note(freq, duree, 5, 0.55) * env(n, 0.005, 0.22)


def pad(freqs, duree):
    n = int(duree * SR); x = np.arange(n) / SR
    s = sum(note(f, duree, 4, 0.5) + note(f * 1.004, duree, 4, 0.5) for f in freqs)
    enveloppe = np.minimum(1, x / 0.4) * np.minimum(1, (duree - x) / 0.4)
    return s * enveloppe / (2 * len(freqs))


def pluck(freq):
    n = int(0.3 * SR)
    return note(freq, 0.3, 3, 0.35) * env(n, 0.002, 0.09)


# Grille d'accords : La mineur – Fa – Do – Sol, un accord par mesure (2 s)
ACCORDS = [(55.0, [220.0, 261.63, 329.63]), (43.65, [174.61, 220.0, 261.63]),
           (65.41, [261.63, 329.63, 392.0]), (49.0, [196.0, 246.94, 293.66])]


s = T["scenes"]
SECTIONS = getattr(MINUTAGE, "SECTIONS", {"intro_fin": s[1], "pauses": [[s[3], s[4]]], "fin_debut": s[7]})


def section(t):
    if t < SECTIONS["intro_fin"]: return "intro"
    if any(a <= t < b for a, b in SECTIONS["pauses"]): return "pause"
    if t >= SECTIONS["fin_debut"]: return "fin"
    return "plein"


def musique():
    buf = piste()
    nb_temps = int(DUREE / TEMPS)
    for b in range(nb_temps):
        t = b * TEMPS
        mesure = b // 4
        racine, accord = ACCORDS[mesure % 4]
        sec = section(t)
        if b % 4 == 0:
            placer(buf, t, pad(accord, 2.0), 0.55 if sec in ("intro", "pause", "fin") else 0.32, 0)
        if sec in ("plein",) or (sec == "fin" and t < DUREE - 2):
            placer(buf, t, kick(), 0.95)
            if b % 2 == 1:
                placer(buf, t, clap(), 0.45)
        for k in (0, 1):  # croches
            tt = t + k * TEMPS / 2
            if sec != "pause":
                placer(buf, tt, charleston(ouvert=(k == 1)), 0.16 if k else 0.12, pan=0.35)
            if sec == "plein":
                placer(buf, tt, basse(racine * (2 if k else 1), 0.24), 0.55)
        if sec == "plein":  # arpège en doubles croches
            for k in range(4):
                placer(buf, t + k * TEMPS / 4, pluck(accord[(b * 4 + k) % 3] * 2), 0.1, pan=-0.3 if k % 2 else 0.3)
        if sec == "pause" and b % 4 == 0:
            placer(buf, t, basse(racine, 1.9) * np.exp(-np.arange(int(1.9 * SR)) / SR * 0.8), 0.6)
    # léger élargissement stéréo, puis fondu final
    buf[:, 1] = np.roll(buf[:, 1], int(0.011 * SR))
    fondu = np.ones(N); fondu[-int(2.0 * SR):] = np.linspace(1, 0, int(2.0 * SR))
    return buf * fondu[:, None]


# ---------------- Effets sonores ----------------
def whoosh(duree=0.5):
    n = int(duree * SR); x = np.linspace(0, 1, n)
    return bruit_filtre(n, 250, 4500) * np.sin(np.pi * x) ** 2


def pop(f0=420, f1=950):
    n = int(0.11 * SR); x = np.arange(n) / SR
    freq = f0 + (f1 - f0) * (1 - np.exp(-x * 40))
    return np.sin(2 * np.pi * np.cumsum(freq) / SR) * env(n, 0.001, 0.04)


def tic():
    n = int(0.02 * SR)
    return np.sin(2 * np.pi * 2400 * np.arange(n) / SR) * env(n, 0.0005, 0.004)


def impact():
    n = int(1.6 * SR); x = np.arange(n) / SR
    sub = np.sin(2 * np.pi * np.cumsum(38 + 80 * np.exp(-x * 9)) / SR) * np.exp(-x * 2.2)
    return np.tanh(2.2 * sub) * 0.9 + bruit_filtre(n, 80, 5000) * env(n, 0.001, 0.12) * 0.6


def montee(duree):
    n = int(duree * SR); x = np.linspace(0, 1, n)
    return bruit_filtre(n, 1500, 9000) * x ** 2.5 + note(220, duree, 3) * 0 + \
        np.sin(2 * np.pi * np.cumsum(200 + 600 * x) / SR) * x ** 2 * 0.25


def carillon():
    sons = []
    for i, f in enumerate((880.0, 1046.5, 1318.5)):
        n = int(1.2 * SR); x = np.arange(n) / SR
        sons.append((i * 0.12, (np.sin(2 * np.pi * f * x) + 0.3 * np.sin(2 * np.pi * f * 2.01 * x)) * env(n, 0.002, 0.45)))
    return sons


def instants_compteur(debut, fin, valeur_max, nb=22):
    """Un tic à chaque palier du compteur (qui ralentit, comme l'animation : 1 - (1 - x)^3)."""
    paliers = np.linspace(0, 1, nb)[1:]
    x = 1 - (1 - paliers) ** (1 / 3)
    return debut + x * (fin - debut)


def effets():
    buf = piste(); s = T["scenes"]
    for b in s[1:8]:                                 # volets de transition
        placer(buf, b - 0.25, whoosh(0.5), 0.5)
    placer(buf, 0.0, whoosh(0.6), 0.45)              # ouverture des deux camps
    placer(buf, T["vs"], pop(300, 700), 0.55)
    for t in instants_compteur(*T["compteurs"], 106):
        placer(buf, t, tic(), 0.35)
    placer(buf, T["medaillon"], pop(), 0.55)
    for i in range(18):                              # atterrissage des tuiles
        placer(buf, T["tuiles"] + i * T["tuile_dt"] + T["tuile_duree"] * 0.55, pop(500 + 15 * i, 800 + 15 * i), 0.22,
               pan=(i % 6 - 2.5) / 4)
    for t in instants_compteur(*T["hero3"], 11, nb=11):
        placer(buf, t, tic(), 0.35)
    placer(buf, T["choc"], montee(T["impact"] - T["choc"]), 0.5)
    placer(buf, T["impact"], impact(), 0.95)
    for i in range(5):
        for decal in (0, 0.09):
            placer(buf, T["pastilles5"] + i * T["pastille_dt"] + decal, pop(600, 1100), 0.22, pan=-0.4 if decal == 0 else 0.4)
    placer(buf, T["egalite"], pop(350, 800), 0.5)
    for i in range(3):
        placer(buf, T["points6"] + i * T["point_dt"], whoosh(0.35), 0.25)
    placer(buf, T["barres7"], montee(2.2), 0.35)
    placer(buf, T["score7"], impact()[: int(0.8 * SR)], 0.55)
    for decal, son in carillon():
        placer(buf, T["appel8"] + decal, son, 0.3)
    return buf


def effets_listes(liste):
    """Effets décrits dans le minutage : (instant, nom, gain[, pan])."""
    sons = {"whoosh": lambda: whoosh(0.5), "whoosh_court": lambda: whoosh(0.35), "pop": pop, "pop_grave": lambda: pop(300, 700),
            "pop_aigu": lambda: pop(600, 1100), "tic": tic, "impact": impact, "impact_court": lambda: impact()[: int(0.8 * SR)]}
    buf = piste()
    for e in liste:
        t, nom, gain = e[:3]
        pan = e[3] if len(e) > 3 else 0.0
        if nom.startswith("montee:"):
            placer(buf, t, montee(float(nom.split(":")[1])), gain, pan)
        elif nom == "carillon":
            for decal, son in carillon():
                placer(buf, t + decal, son, gain, pan)
        else:
            placer(buf, t, sons[nom](), gain, pan)
    return buf


def charger_musique(chemin):
    """Convertit un morceau externe (mp3, wav…) en 44,1 kHz stéréo, coupé à la durée de la vidéo."""
    import imageio_ffmpeg
    brut = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-loglevel", "error", "-i", chemin, "-t", str(DUREE),
                           "-f", "s16le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    m = np.frombuffer(brut, dtype=np.int16).reshape(-1, 2) / 32768.0
    buf = piste(); buf[:len(m)] = m[:N]
    fondu = np.ones(N); fondu[-int(2 * SR):] = np.linspace(1, 0, int(2 * SR))
    return buf * fondu[:, None] * 0.7


def ecrire(chemin, buf):
    with wave.open(str(chemin), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(buf, -1, 1) * 32767).astype(np.int16).tobytes())


if __name__ == "__main__":
    m = charger_musique(ARGS[1]) if len(ARGS) > 1 and ARGS[0] == "--musique" else musique()
    e = effets_listes(MINUTAGE.EFFETS) if hasattr(MINUTAGE, "EFFETS") else effets()
    m /= np.abs(m).max() + 1e-9; e /= np.abs(e).max() + 1e-9
    mix = np.tanh(1.1 * (0.62 * m + 0.75 * e))
    mix *= 0.89 / np.abs(mix).max()   # crête à -1 dB
    ecrire(ICI / CONF["audio"], mix)
    print(CONF["audio"], "écrit :", DUREE, "s")
