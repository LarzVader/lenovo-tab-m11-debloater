#!/bin/sh
# Lenovo Tab M11 Debloater - start on Linux / Start unter Linux
cd "$(dirname "$0")" || exit 1
if command -v python3 >/dev/null 2>&1; then
    exec python3 ./m11_debloater.py "$@"
fi
echo "Python 3 was not found. Install it with your package manager, e.g.: sudo apt install python3"
echo "Python 3 wurde nicht gefunden. Installiere es mit deiner Paketverwaltung, z. B.: sudo apt install python3"
exit 1
