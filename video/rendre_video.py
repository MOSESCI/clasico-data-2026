"""Capture scene.html image par image (Chrome via Playwright) puis assemble la vidéo MP4 avec le son.

Usage : python video/rendre_video.py            (vidéo complète)
        python video/rendre_video.py --apercu 1.2 4.5 13   (quelques images PNG pour vérifier)
"""
import subprocess, sys
from pathlib import Path
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
from minutage import FPS, DUREE

ICI = Path(__file__).parent
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def ouvrir(p):
    nav = p.chromium.launch(channel="chrome")
    page = nav.new_page(viewport={"width": 1080, "height": 1920})
    page.goto((ICI / "scene.html").as_uri())
    page.wait_for_load_state("networkidle")
    page.evaluate("document.fonts.ready")
    return nav, page


if len(sys.argv) > 2 and sys.argv[1] == "--apercu":
    with sync_playwright() as p:
        nav, page = ouvrir(p)
        for t in sys.argv[2:]:
            page.evaluate(f"render({float(t)})")
            page.screenshot(path=str(ICI / f"apercu_{t}.png"))
        nav.close()
    sys.exit()

images = ICI / "images.mp4"
n = int(DUREE * FPS)
enc = subprocess.Popen([FFMPEG, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", str(images)],
                       stdin=subprocess.PIPE)
with sync_playwright() as p:
    nav, page = ouvrir(p)
    for i in range(n):
        page.evaluate(f"render({i / FPS})")
        enc.stdin.write(page.screenshot(type="png"))
        if i % 150 == 0:
            print(f"  image {i}/{n}")
    nav.close()
enc.stdin.close(); enc.wait()

son = ICI / "audio.wav"
sortie = ICI / "clasico_reel.mp4"
cmd = [FFMPEG, "-y", "-loglevel", "error", "-i", str(images)]
cmd += (["-i", str(son), "-c:a", "aac", "-b:a", "192k", "-shortest"] if son.exists() else [])
cmd += ["-c:v", "copy", "-movflags", "+faststart", str(sortie)]
subprocess.run(cmd, check=True)
images.unlink()
print("Vidéo :", sortie)
