// Web de la exposición: funciona sin conexión.
// - Páginas (index, iconos…): primero la red, para tener siempre la versión más reciente; sin red, la copia guardada.
// - Fotos: se guardan una vez en una caché propia que NO se borra al actualizar la web. La primera visita las descarga todas.
const CACHE = "minerales-20261117100333";
const FOTOS = "minerales-fotos";
const ARCHIVOS = ["./", "./index.html", "./index_en.html", "./manifest.webmanifest", "./icono-180.png", "./icono-192.png", "./icono-512.png", "./lista-fotos.json"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(ARCHIVOS))); self.skipWaiting(); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE && k !== FOTOS).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
const esFoto = u => u.pathname.includes("/FICHAS%20DE%20MINERALES/") || u.pathname.includes("/FICHAS DE MINERALES/");
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  const u = new URL(e.request.url);
  if (u.origin !== location.origin) return;
  if (esFoto(u)) {
    e.respondWith(caches.open(FOTOS).then(c => c.match(e.request).then(r => r || fetch(e.request).then(n => { if (n.ok) c.put(e.request, n.clone()); return n; }))));
    return;
  }
  e.respondWith(fetch(e.request).then(r => {
    if (r.ok) { const copia = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copia)); }
    return r;
  }).catch(() => caches.match(e.request).then(r => r || caches.match("./index.html"))));
});
// Descarga de todas las fotos (la pide la página). Informa del progreso a la página.
let enMarcha = false;
self.addEventListener("message", e => {
  if (!e.data || e.data.tipo !== "precargar" || enMarcha) return;
  enMarcha = true;
  e.waitUntil((async () => {
    const lista = await (await fetch("./lista-fotos.json", { cache: "no-store" })).json();
    const c = await caches.open(FOTOS);
    let hechas = 0;
    const avisa = async fin => { for (const cl of await self.clients.matchAll()) cl.postMessage({ tipo: "progreso", hechas, total: lista.length, fin }); };
    const cola = lista.slice();
    const trabajador = async () => {
      while (cola.length) {
        const ruta = cola.shift();
        try { if (!(await c.match(ruta))) { const r = await fetch(ruta); if (r.ok) await c.put(ruta, r); } } catch (_) {}
        hechas++; if (hechas % 25 === 0) await avisa(false);
      }
    };
    await Promise.all([1, 2, 3, 4, 5, 6].map(trabajador));
    await avisa(true); enMarcha = false;
  })());
});
