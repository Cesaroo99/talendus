# Applis Talendus (Android et iPhone)

Une fois installée, l’appli ouvre la coque mobile (`/m.html`) : accueil, offres, messages et compte. Ce n’est plus le site public.

Fichiers d’installation :

- Android : `assets/app/talendus.apk` via `/download/talendus.apk`
- iPhone : `assets/app/talendus.mobileconfig` via `/download/talendus.mobileconfig`

Pour reconstruire l’APK :

```bash
export ANDROID_HOME="$HOME/android-sdk"
python3 scripts/build_install_packages.py
bash scripts/build_android_apk.sh
```
