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
# Las fotos se guardan en el aparato a medida que se abren las fichas (no se descargan todas de golpe, para no gastar datos).
registro = '<script>if ("serviceWorker" in navigator && /github\\.io$/.test(location.hostname)) navigator.serviceWorker.register("sw.js");</script>\n'
www = aqui.parent / "www"
for f in ["manifest.webmanifest", "icono-180.png", "icono-192.png", "icono-512.png"]:
    shutil.copy(aqui / "pwa" / f, www / f)
(www / "sw.js").write_text((aqui / "pwa" / "sw.js").read_text(encoding="utf-8").replace("VERSION", time.strftime("%Y%m%d%H%M%S")), encoding="utf-8")
# Botón «Descargar la app para Android»: solo en la web (no dentro de la app) y solo en aparatos Android.
APK = "https://github.com/ALG865/Minerales-app/releases/latest/download/minerales-estrategicos.apk"
texto_apk = "Download the Android app" if salida.endswith("_en.html") else "Descargar la app para Android"
boton_apk = ('<script>(function(){if(window.Capacitor||!/Android/i.test(navigator.userAgent))return;'
  'var c=document.querySelector("#home .home-content");if(!c)return;var a=document.createElement("a");'
  'a.href="%s";a.className="boton-apk";a.textContent="%s";a.setAttribute("download","");c.appendChild(a);})();</script>\n'
  '<style>.boton-apk{display:inline-flex;align-items:center;gap:.5em;margin:1.2rem auto 0;padding:.75em 1.4em;border-radius:999px;'
  'background:#3ddc84;color:#0d263d;font:700 1rem Arial,sans-serif;text-decoration:none;box-shadow:0 4px 14px rgba(0,0,0,.35)}'
  '.boton-apk::before{content:"\\2193";font-size:1.2em}</style>\n') % (APK, texto_apk)
# Mapa «¿Qué produce cada país?» en el móvil: puntos más pequeños (proporcionales al mapa) y un desplegable para elegir país.
texto_sel = ("Choose a country" if salida.endswith("_en.html") else "Elige un país")
selector = ('<script>(function(){var m=document.getElementById("paisesMapa");if(!m)return;'
  'var sel=document.createElement("select");sel.className="paises-selector";sel.setAttribute("aria-label","%s");'
  'm.parentNode.insertBefore(sel,m);'
  'function ajusta(){var ds=[].slice.call(m.querySelectorAll(".prod-punto"));if(!ds.length)return;'
  'var f=Math.max(.4,Math.min(1,m.clientWidth/1000));ds.forEach(function(d){if(!d.dataset.t0)d.dataset.t0=parseFloat(d.style.width)||12;var t=Math.max(7,d.dataset.t0*f);d.style.width=d.style.height=t+"px";});'
  'var ps=ds.map(function(d){return d.dataset.pais}).sort(function(a,b){return a.localeCompare(b)});'
  'var act=(m.querySelector(".prod-punto.actual")||{}).dataset;'
  'sel.innerHTML="<option value=\\"\\">%s…</option>"+ps.map(function(p){return "<option>"+p+"</option>"}).join("");'
  'if(act&&act.pais)sel.value=act.pais;}'
  'sel.addEventListener("change",function(){var d=[].slice.call(m.querySelectorAll(".prod-punto")).filter(function(x){return x.dataset.pais===sel.value})[0];if(d)d.click();});'
  'new MutationObserver(function(){ajusta()}).observe(m,{childList:true,subtree:true,attributes:true,attributeFilter:["class"]});'
  'window.addEventListener("resize",ajusta);})();</script>\n'
  '<style>.paises-selector{display:none;width:100%%;margin:0 0 10px;padding:10px 12px;font:600 16px Arial,sans-serif;border-radius:10px;border:2px solid #c99b45;background:#f4f1e9;color:#0d263d}'
  '@media (max-width:1100px){.paises-selector{display:block}}</style>\n') % (texto_sel, texto_sel)
# Mapa de «Producción mundial» en el móvil: burbujas proporcionales al mapa y etiquetas que no se salen por los lados.
mapas_prod = ('<script>(function(){var m=document.getElementById("produccionMapa");if(!m)return;'
  'function ajusta(){var ds=[].slice.call(m.querySelectorAll(".prod-punto"));if(!ds.length)return;'
  'var f=Math.max(.45,Math.min(1,m.clientWidth/900));'
  'ds.forEach(function(d){if(!d.dataset.t0)d.dataset.t0=parseFloat(d.style.width)||12;var t=Math.max(8,d.dataset.t0*f);if(Math.abs(parseFloat(d.style.width)-t)>.5)d.style.width=d.style.height=t+"px";});'
  'var R=m.getBoundingClientRect();ds.forEach(function(d){var sp=d.querySelector("span");if(!sp)return;'
  'var q=sp.getBoundingClientRect();if(q.right>R.right-2&&!d.classList.contains("etiqueta-izq")){d.classList.remove("etiqueta-abajo");d.classList.add("etiqueta-izq");q=sp.getBoundingClientRect();}'
  'if(q.left<R.left+2){d.classList.remove("etiqueta-izq");d.classList.add("etiqueta-abajo");q=sp.getBoundingClientRect();}'
  'if(q.bottom>R.bottom-1){sp.style.top="auto";sp.style.bottom="100%";}});'
  'var sps=ds.map(function(d){return d.querySelector("span")}).filter(Boolean);'
  'function cruza(a,b){var x=a.getBoundingClientRect(),y=b.getBoundingClientRect();return !(x.right<y.left||y.right<x.left||x.bottom<y.top||y.bottom<x.top);}'
  'for(var i=0;i<sps.length;i++)for(var j=0;j<i;j++){if(cruza(sps[i],sps[j])){var d=sps[i].parentNode;d.classList.remove("etiqueta-izq");d.classList.add("etiqueta-abajo");'
  'var q=sps[i].getBoundingClientRect();if(q.left<R.left+2)sps[i].style.transform="translate(-"+Math.max(0,50-100*(d.getBoundingClientRect().left-R.left)/q.width)+"%,3px)";'
  'if(q.right>R.right-2)sps[i].style.transform="translate(-"+Math.min(100,50+100*(q.right-R.right+4)/q.width)+"%,3px)";'
  'if(cruza(sps[i],sps[j]))sps[i].style.top="auto",sps[i].style.bottom="100%";'
  'if(cruza(sps[i],sps[j]))sps[i].style.visibility="hidden";}}}'
  'var pend=0;new MutationObserver(function(){if(pend)return;pend=requestAnimationFrame(function(){pend=0;ajusta();});}).observe(m,{childList:true});'
  'window.addEventListener("resize",ajusta);document.addEventListener("click",function(){setTimeout(ajusta,60);},true);})();</script>\n'
  '<style>@media (max-width:700px){.prod-mapa .prod-punto span{font-size:11px!important}}'
  '.prod-mapa .prod-punto{transform:translate(-50%,-50%) scale(var(--inv,1))!important}'
  '.pista-zoom{display:none;margin:6px 0 0;font:13px Arial,sans-serif;color:#5a6b7b;text-align:center}'
  '@media (max-width:1100px){.pista-zoom{display:block}}</style>\n'
  '<script>' + (aqui / "zoom_mapas.js").read_text(encoding="utf-8") + '</script>\n'
  '<script>(function(){var t=%s;["paisesMapa","produccionMapa"].forEach(function(id){var m=document.getElementById(id);if(!m)return;var p=document.createElement("p");p.className="pista-zoom";p.textContent=t;m.parentNode.parentNode.insertBefore(p,m.parentNode.nextSibling);});})();</script>\n' % ('"Pinch with two fingers to zoom in on the map; double-tap to go back"' if salida.endswith("_en.html") else '"Pellizca con dos dedos para ampliar el mapa; doble toque para volver"'))
i = s.rindex('</body>')
s = s[:i] + registro + boton_apk + selector + mapas_prod + s[i:]
s = s[:i] + '<style id="ajustes-movil">\n' + css + '\n</style>\n' + s[i:]
salida = sys.argv[2] if len(sys.argv) > 2 else "index.html"
en = salida.endswith("_en.html")
if en:
    s = s.replace('<html lang="es">', '<html lang="en">', 1)
(aqui.parent / "www" / salida).write_text(s, encoding="utf-8")
print("www/index.html listo")
