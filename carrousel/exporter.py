"""Exporte un carrousel HTML en PDF (pour LinkedIn) et en images PNG, une par slide.

Usage : python carrousel/exporter.py carrousel/post1_pronostic.html
Nécessite Google Chrome (ou Microsoft Edge) installé.
"""
import os, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image

NAVIGATEURS = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
               r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]
LARGEUR, HAUTEUR = 1080, 1350

html = Path(sys.argv[1]).resolve()
navigateur = next(n for n in NAVIGATEURS if os.path.exists(n))
nb_slides = html.read_text(encoding="utf-8").count('<section class="slide')
profil = tempfile.mkdtemp()
commun = [navigateur, "--headless=new", "--disable-gpu", f"--user-data-dir={profil}",
          "--hide-scrollbars", "--virtual-time-budget=10000"]

pdf = html.with_suffix(".pdf")
subprocess.run(commun + ["--no-pdf-header-footer", f"--print-to-pdf={pdf}", html.as_uri()], check=True)

capture = Path(profil) / "capture.png"
subprocess.run(commun + [f"--window-size={LARGEUR},{HAUTEUR * nb_slides}", f"--screenshot={capture}", html.as_uri()], check=True)
dossier = html.with_suffix("")
dossier.mkdir(exist_ok=True)
for ancienne in dossier.glob("slide_*.png"):
    ancienne.unlink()
image = Image.open(capture)
for i in range(nb_slides):
    image.crop((0, i * HAUTEUR, LARGEUR, (i + 1) * HAUTEUR)).save(dossier / f"slide_{i + 1:02d}.png")
print(f"{pdf.name} + {nb_slides} images dans {dossier.name}/")
