"""Minutage unique de la vidéo (en secondes), partagé par l'animation (scene.html) et le son (audio.py).

Modifier un temps ici décale à la fois l'image et le son : ils restent synchronisés.
"""
FPS = 30
DUREE = 36.0

T = {
    "scenes": [0, 3, 7, 12, 15, 20, 25, 31, 36],   # début de chaque scène, puis la fin
    "vs": 0.6,                                     # 1 · apparition du « VS »
    "titre1": 0.95,
    "compteurs": [3.3, 5.0],                       # 2 · compteurs 0 → 106
    "medaillon": 5.2, "legende2": 5.6,
    "tuiles": 7.5, "tuile_dt": 0.12, "tuile_duree": 0.35,   # 3 · 18 tuiles
    "hero3": [9.9, 10.7],
    "choc": 12.15, "impact": 12.45,                # 4 · le « 0 » qui tombe
    "cartes5": [15.2, 15.35], "pastilles5": 15.9, "pastille_dt": 0.18, "egalite": 18.0,
    "anneaux6": 20.6, "points6": 21.0, "point_dt": 0.35, "point_duree": 0.8,   # 6 · joueurs
    "barres7": 25.5, "barre_dt": 0.3, "barre_duree": 1.2, "score7": 28.0, "marche7": 28.6,
    "appel8": 32.2,
}
