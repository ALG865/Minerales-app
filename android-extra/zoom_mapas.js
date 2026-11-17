// Zoom con dos dedos dentro de los mapas del mundo (móvil y tableta). Al ampliar, los puntos y sus
// etiquetas mantienen su tamaño en pantalla, así que quedan proporcionalmente más pequeños y se
// separan. Un dedo mueve el mapa cuando está ampliado; doble toque vuelve al tamaño normal.
(function () {
  ["paisesMapa", "produccionMapa"].forEach(function (id) {
    var m = document.getElementById(id); if (!m) return;
    var marco = m.parentNode; marco.style.overflow = "hidden";
    m.style.transformOrigin = "0 0"; m.style.touchAction = "pan-y";
    var s = 1, tx = 0, ty = 0, ini = null, ultimoToque = 0, movido = false;
    function limita() {
      var W = m.offsetWidth, H = m.offsetHeight;
      tx = Math.min(0, Math.max(W - W * s, tx)); ty = Math.min(0, Math.max(H - H * s, ty));
    }
    function aplica() {
      limita();
      m.style.transform = s > 1.001 ? "translate(" + tx + "px," + ty + "px) scale(" + s + ")" : "";
      m.style.setProperty("--inv", 1 / s);
      m.style.touchAction = s > 1.001 ? "none" : "pan-y";
    }
    function dist(t) { return Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY); }
    function centro(t) { var r = m.parentNode.getBoundingClientRect(); return [(t[0].clientX + t[1].clientX) / 2 - r.left, (t[0].clientY + t[1].clientY) / 2 - r.top]; }
    m.addEventListener("touchstart", function (e) {
      movido = false;
      if (e.touches.length === 2) { var c = centro(e.touches); ini = { d: dist(e.touches), s: s, cx: c[0], cy: c[1], tx: tx, ty: ty }; }
      else if (e.touches.length === 1 && s > 1.001) { ini = { x: e.touches[0].clientX, y: e.touches[0].clientY, tx: tx, ty: ty }; }
    }, { passive: true });
    m.addEventListener("touchmove", function (e) {
      if (!ini) return;
      if (e.touches.length === 2 && ini.d) {
        e.preventDefault(); movido = true;
        var c = centro(e.touches), ns = Math.max(1, Math.min(8, ini.s * dist(e.touches) / ini.d));
        // el punto del mapa bajo los dedos se queda bajo los dedos
        var mx = (ini.cx - ini.tx) / ini.s, my = (ini.cy - ini.ty) / ini.s;
        s = ns; tx = c[0] - mx * s; ty = c[1] - my * s; aplica();
      } else if (e.touches.length === 1 && ini.x != null && s > 1.001) {
        e.preventDefault(); movido = true;
        tx = ini.tx + e.touches[0].clientX - ini.x; ty = ini.ty + e.touches[0].clientY - ini.y; aplica();
      }
    }, { passive: false });
    m.addEventListener("touchend", function (e) {
      if (e.touches.length === 0) {
        var ahora = Date.now();
        if (!movido && ahora - ultimoToque < 300) { s = 1; tx = ty = 0; aplica(); }
        ultimoToque = ahora; ini = null;
      } else if (e.touches.length === 1 && s > 1.001) { ini = { x: e.touches[0].clientX, y: e.touches[0].clientY, tx: tx, ty: ty }; }
    });
    // si se ha arrastrado, que no cuente como pulsar un punto
    m.addEventListener("click", function (e) { if (movido) { e.stopPropagation(); e.preventDefault(); movido = false; } }, true);
    // al volver a dibujar el mapa (otro país o materia), se mantiene el zoom; al entrar en la pantalla, se reinicia
    new MutationObserver(function () { m.style.setProperty("--inv", 1 / s); }).observe(m, { childList: true });
    document.addEventListener("click", function (e) { if (e.target.closest && e.target.closest(".productores-clicable, #produccionVerPaises")) { s = 1; tx = ty = 0; aplica(); } }, true);
  });
})();
