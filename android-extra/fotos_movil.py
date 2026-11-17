"""Copia a www/ las fotos que usa la web, reducidas para el móvil: 1000 px (miniaturas 300 px), WebP 75.
Uso: python3 android-extra/fotos_movil.py <carpeta de la web> www/index.html"""
import sys, re, os, pathlib
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
web = pathlib.Path(sys.argv[1]); html = pathlib.Path(sys.argv[2]).read_text(encoding="utf-8")
www = pathlib.Path(sys.argv[2]).parent
rutas = sorted(set(re.findall(r'"(FICHAS DE MINERALES/imagenes/[^"]+\.webp)"', html)))
def hace(r):
    o, d = web / r, www / r
    if d.exists() and d.stat().st_mtime >= o.stat().st_mtime: return 0
    d.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(o); lado = 300 if "/miniaturas/" in r else 1000
    im.thumbnail((lado, lado), Image.LANCZOS); im.save(d, "WEBP", quality=75, method=6)
    return 1
if __name__ == "__main__":
    falta = [r for r in rutas if not (web / r).exists()]
    assert not falta, falta[:5]
    with ProcessPoolExecutor(8) as ex: n = sum(ex.map(hace, rutas, chunksize=20))
    usadas = set(rutas)
    for p in (www / "FICHAS DE MINERALES").rglob("*.webp"):
        if str(p.relative_to(www)) not in usadas: p.unlink()
    import json
    (www / "lista-fotos.json").write_text(json.dumps([__import__("urllib.parse").parse.quote(r) for r in rutas]), encoding="utf-8")
    print(len(rutas), "fotos;", n, "nuevas o cambiadas")
