"""Hace que el APK se firme siempre con la misma clave (android-extra/debug.keystore)
y pone el número de versión. Uso: python3 android-extra/patch_gradle.py <numero>"""
import re, sys, os
n = sys.argv[1]
p = 'android/app/build.gradle'
s = open(p).read()
ks = os.path.abspath('android-extra/debug.keystore')
s = re.sub(r'versionCode \d+', f'versionCode {n}', s)
s = re.sub(r'versionName "[^"]*"', f'versionName "0.{n}"', s)
firma = f'''
    signingConfigs {{
        fija {{
            storeFile file("{ks}")
            storePassword "android"
            keyAlias "androiddebugkey"
            keyPassword "android"
        }}
    }}
'''
s = s.replace('android {', 'android {' + firma, 1)
if 'buildTypes {' in s:
    s = s.replace('buildTypes {', 'buildTypes {\n        debug {\n            signingConfig signingConfigs.fija\n        }', 1)
else:
    s = s.replace(firma, firma + '    buildTypes {\n        debug {\n            signingConfig signingConfigs.fija\n        }\n    }\n', 1)
open(p, 'w').write(s)
print(s[:1500])
