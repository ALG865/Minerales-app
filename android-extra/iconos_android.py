"""Pone el icono de la exposición (android-extra/pwa/icono-1024.png) como icono de la app Android."""
import pathlib, re
from PIL import Image
res = pathlib.Path("android/app/src/main/res")
src = Image.open("android-extra/pwa/icono-1024.png").convert("RGBA")
for d, n in {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}.items():
    carpeta = res / f"mipmap-{d}"; carpeta.mkdir(parents=True, exist_ok=True)
    for nombre in ("ic_launcher.png", "ic_launcher_round.png"):
        src.resize((n, n), Image.LANCZOS).save(carpeta / nombre)
    f = round(n * 108 / 48)
    src.resize((f, f), Image.LANCZOS).save(carpeta / "ic_launcher_foreground.png")
for p in res.rglob("ic_launcher_background.xml"):
    s = p.read_text(); p.write_text(re.sub(r'#[0-9A-Fa-f]{6,8}', '#0D263D', s))
print("iconos listos")
