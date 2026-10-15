"""Prepara www/index.html a partir de la copia ligera de la web.
Uso: python3 android-extra/preparar_www.py <copia_ligera.html>
- Inserta los ajustes de móvil (android-extra/ajustes-movil.css) al final del body.
- Permite el zoom con dos dedos (viewport y touch-action)."""
import sys, pathlib
aqui = pathlib.Path(__file__).parent
s = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
css = (aqui / "ajustes-movil.css").read_text(encoding="utf-8")
def rep(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)
rep('content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"',
    'content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes"')
rep('html, body { touch-action: pan-x pan-y;', 'html, body { touch-action: manipulation;')
# En el móvil no se pide pantalla completa: en ese modo Android deja de permitir el zoom con dos dedos.
rep('var PANTALLA_COMPLETA = true;', 'var PANTALLA_COMPLETA = false;')
i = s.rindex('</body>')
s = s[:i] + '<style id="ajustes-movil">\n' + css + '\n</style>\n' + s[i:]
(aqui.parent / "www" / "index.html").write_text(s, encoding="utf-8")
print("www/index.html listo")
