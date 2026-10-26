"""Les vidéos du projet. Chaque vidéo a son minutage, sa scène, sa bande son et son fichier de sortie.

Les scripts acceptent « --projet <nom> » (par défaut : reel, la vidéo d'avant-match).
"""
import importlib

PROJETS = {
    "reel": {"minutage": "minutage", "scene": "scene.html", "audio": "audio.wav", "sortie": "clasico_reel.mp4"},
    "verdict": {"minutage": "minutage_verdict", "scene": "scene_verdict.html", "audio": "audio_verdict.wav",
                "sortie": "clasico_verdict.mp4"},
}


def choisir(argv):
    """Retire « --projet <nom> » des arguments et renvoie (nom, configuration, module de minutage)."""
    nom = "reel"
    if "--projet" in argv:
        i = argv.index("--projet")
        nom = argv[i + 1]
        del argv[i:i + 2]
    conf = PROJETS[nom]
    return nom, conf, importlib.import_module(conf["minutage"])
