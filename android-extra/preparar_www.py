"""Prepara www/index.html a partir de la copia ligera de la web.
Uso: python3 android-extra/preparar_www.py <copia_ligera.html> [index.html|index_en.html]
- Inserta los ajustes de móvil (android-extra/ajustes-movil.css) al final del body.
- Permite el zoom con dos dedos (viewport y touch-action)."""
import sys, pathlib
salida = sys.argv[2] if len(sys.argv) > 2 else "index.html"
aqui = pathlib.Path(__file__).parent
s = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
css = (aqui / "ajustes-movil.css").read_text(encoding="utf-8")
def rep(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)
# La bandera de idioma: en la dirección raíz («/») el archivo es index.html.
rep('decodeURIComponent(location.pathname.split("/").pop() || "")', 'decodeURIComponent(location.pathname.split("/").pop() || "index.html")')
rep('content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"',
    'content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes"')
rep('html, body { touch-action: pan-x pan-y;', 'html, body { touch-action: manipulation;')
# En iPhone, los eventos gesture* bloquean el zoom con dos dedos: no se anulan.
rep('document.addEventListener(t, function (e) { e.preventDefault(); });', 'void t;')
# En el móvil no se pide pantalla completa: en ese modo Android deja de permitir el zoom con dos dedos.
rep('var PANTALLA_COMPLETA = true;', 'var PANTALLA_COMPLETA = false;')
# Instalable en iPhone/iPad (y Android) desde el navegador: icono, nombre y uso sin conexión.
import re, shutil, time
s = re.sub(r'<title>[^<]*</title>', '<title>Minerales estratégicos y críticos</title>' if not salida.endswith('_en.html') else '<title>Strategic and critical minerals</title>', s, count=1)
cabecera = '''<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icono-180.png">
<link rel="icon" type="image/png" href="icono-192.png">
<meta name="theme-color" content="#0d263d">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<meta name="apple-mobile-web-app-title" content="Minerales">
'''
rep('<meta charset="utf-8"/>', '<meta charset="utf-8"/>\n' + cabecera)
registro = '<script>if ("serviceWorker" in navigator && /github\\.io$/.test(location.hostname)) navigator.serviceWorker.register("sw.js");</script>\n'
www = aqui.parent / "www"
for f in ["manifest.webmanifest", "icono-180.png", "icono-192.png", "icono-512.png"]:
    shutil.copy(aqui / "pwa" / f, www / f)
(www / "sw.js").write_text((aqui / "pwa" / "sw.js").read_text(encoding="utf-8").replace("VERSION", time.strftime("%Y%m%d%H%M%S")), encoding="utf-8")
i = s.rindex('</body>')
s = s[:i] + registro + s[i:]
s = s[:i] + '<style id="ajustes-movil">\n' + css + '\n</style>\n' + s[i:]
salida = sys.argv[2] if len(sys.argv) > 2 else "index.html"
en = salida.endswith("_en.html")
if en:
    s = s.replace('<html lang="es">', '<html lang="en">', 1)
(aqui.parent / "www" / salida).write_text(s, encoding="utf-8")
print("www/index.html listo")
