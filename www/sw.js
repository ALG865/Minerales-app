// Web de la exposición: funciona sin conexión.
// - Páginas (index, iconos…): primero la red, para tener siempre la versión más reciente; sin red, la copia guardada.
// - Fotos: cada foto que se abre se guarda en una caché propia que NO se borra al actualizar la web (no se descargan todas de golpe).
const CACHE = "minerales-20261118111719";
const FOTOS = "minerales-fotos";
const ARCHIVOS = ["./", "./index.html", "./index_en.html", "./manifest.webmanifest", "./icono-180.png", "./icono-192.png", "./icono-512.png"];
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
  e.respondWith(fetch(e.request, { cache: "no-cache" }).then(r => {   // sin caché HTTP: siempre la última versión publicada
    if (r.ok) { const copia = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copia)); }
    return r;
  }).catch(() => caches.match(e.request).then(r => r || caches.match("./index.html"))));
});
