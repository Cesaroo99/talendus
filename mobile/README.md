# Applis Talendus (Android et iPhone)

Le site sert des fichiers d’installation réels :

- Android : `assets/app/talendus.apk`, téléchargé via `/download/talendus.apk`
- iPhone : `assets/app/talendus.mobileconfig`, téléchargé via `/download/talendus.mobileconfig`

Le bouton **Installer** télécharge ce fichier. Ce n’est pas un guide d’étapes à suivre dans le navigateur.

Pour reconstruire l’APK :

```bash
export ANDROID_HOME="$HOME/android-sdk"
python3 scripts/build_install_packages.py
bash scripts/build_android_apk.sh
```
