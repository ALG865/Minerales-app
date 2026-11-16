# Minerales estratégicos — app Android

App de la exposición de minerales estratégicos y críticos (IACT-CSIC).
Lleva la web completa con todas las fotos, reducidas a 1000 px (miniaturas 300 px) para el móvil.

- Fotos: `python3 android-extra/fotos_movil.py <carpeta de la web> www/index.html`.

- La web está en `www/index.html`.
- Cada vez que se sube un cambio, GitHub genera el APK solo (pestaña **Actions** → «Generar APK» → apartado *Artifacts*).
