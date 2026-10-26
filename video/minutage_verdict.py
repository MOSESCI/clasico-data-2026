"""Minutage de la vidéo du verdict (en secondes), partagé par scene_verdict.html et audio.py."""
FPS = 30
DUREE = 30.0

T = {
    "scenes": [0, 3.5, 7.5, 12, 17, 20.5, 25, 30],
    "titre1": 0.9, "il_a_gagne": 2.0,                       # 1 · « J'avais donné 19 % au Real. Il a gagné. »
    "buts2": [4.0, 4.8, 5.6], "fin2": 6.4,                  # 2 · 0-1, 1-1, 1-2 puis « FIN »
    "jetons3": 8.0, "jeton_dt": 0.15, "allume3": 9.2, "texte3": [9.8, 10.6],   # 3 · 1 chance sur 5
    "barres4": 12.5, "barre_dt": 0.6, "barre_duree": 0.9, "legende4": 15.6,     # 4 · le ballon contre les occasions
    "choc5": 17.3, "impact5": 17.6,                         # 5 · 0 nul en 19 Clásicos
    "compteur6": [21.4, 22.4], "note6": 22.8, "raphinha6": 23.5,               # 6 · Mbappé
    "lecon7": 25.6, "appel7": 27.4,                         # 7 · la leçon
}

# Musique : introduction calme, pause dramatique sur le « 0 », fin apaisée
SECTIONS = {"intro_fin": 3.5, "pauses": [[17.0, 20.5]], "fin_debut": 25.0}

# Effets sonores : (instant, nom, gain[, pan]) — noms définis dans audio.py
EFFETS = (
    [(0.0, "whoosh", 0.45), (T["titre1"], "pop_grave", 0.4), (T["il_a_gagne"], "impact_court", 0.6)]
    + [(b - 0.25, "whoosh", 0.5) for b in T["scenes"][1:7]]
    + [(t, "impact_court", 0.55) for t in T["buts2"]] + [(T["fin2"], "pop", 0.5)]
    + [(T["jetons3"] + i * T["jeton_dt"], "pop_aigu", 0.25, (i - 2) / 3) for i in range(5)]
    + [(T["allume3"], "pop_grave", 0.6), (T["texte3"][1], "pop", 0.35)]
    + [(T["barres4"] + i * T["barre_dt"], "whoosh_court", 0.3) for i in range(4)] + [(T["legende4"], "pop", 0.4)]
    + [(T["choc5"], "montee:0.3", 0.5), (T["impact5"], "impact", 0.95)]
    + [(T["compteur6"][0] + k * 0.1, "tic", 0.3) for k in range(10)] + [(T["compteur6"][1], "impact_court", 0.55),
                                                                         (T["raphinha6"], "pop", 0.35)]
    + [(T["lecon7"], "pop_grave", 0.4), (T["appel7"], "carillon", 0.3)]
)
