# Applis natives Talendus (Android et iOS)

Talendus se lance d’abord comme **application web installable** (PWA) depuis [talendus.ca/app.html](https://talendus.ca/app.html). Android et iPhone l’ajoutent à l’écran d’accueil **sans magasin d’applications**.

Ce dossier contient les **coques natives** (WebView) qui ouvrent le même site. Elles servent si vous compilez un APK ou une archive Xcode en interne, toujours sans Stripe, Twilio ni magasin obligatoire.

## Android

Projet Gradle minimal, paquet `ca.talendus.app`.

1. Ouvrir `mobile/android` dans Android Studio.
2. SDK 26+, Internet autorisé.
3. Run / Build APK. L’appli charge `https://talendus.ca`.

## iOS

Projet SwiftUI + WKWebView.

1. Installer [XcodeGen](https://github.com/yonaskolb/XcodeGen) : `brew install xcodegen`.
2. Dans `mobile/ios` : `xcodegen generate` puis ouvrir `Talendus.xcodeproj`.
3. Signer avec votre équipe Apple et lancer sur simulateur ou appareil.

## Capacitor (option)

`package.json` et `capacitor.config.json` permettent `npx cap add android` / `npx cap add ios` si vous préférez cet outillage. L’URL serveur pointe vers le site Talendus.
