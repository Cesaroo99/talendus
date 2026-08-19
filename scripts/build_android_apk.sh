#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SDK_ROOT="${ANDROID_HOME:-${ANDROID_SDK_ROOT:-$HOME/android-sdk}}"
GRADLE_BIN="${GRADLE_BIN:-/tmp/gradle-8.9/bin/gradle}"
export ANDROID_HOME="$SDK_ROOT"
export ANDROID_SDK_ROOT="$SDK_ROOT"
if [ ! -x "$GRADLE_BIN" ]; then
  echo "Gradle introuvable: $GRADLE_BIN" >&2
  exit 1
fi
if [ ! -d "$SDK_ROOT/platforms/android-34" ]; then
  echo "SDK Android 34 introuvable dans $SDK_ROOT" >&2
  exit 1
fi
python3 "$ROOT/scripts/build_install_packages.py"
"$GRADLE_BIN" -p "$ROOT/mobile/android" assembleDebug --no-daemon
OUT="$ROOT/assets/app/talendus.apk"
mkdir -p "$ROOT/assets/app"
cp -f "$ROOT/mobile/android/app/build/outputs/apk/debug/app-debug.apk" "$OUT"
echo "APK: $OUT"
ls -lh "$OUT"
