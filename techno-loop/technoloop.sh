#!/usr/bin/env bash
# Linux/macOS: ./technoloop.sh setup | keyframes | szenen | vorschau | bauen | song | resolve | demo
set -euo pipefail
cd "$(dirname "$0")"
if [ "${1:-}" = "setup" ]; then
  python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
  mkdir -p musik bilder; [ -f projekt.json ] || cp projekt.example.json projekt.json
  exit 0
fi
PY=.venv/bin/python
case "${1:-}" in
  szenen) shift; exec $PY -m technoloop szenen projekt.json "$@" ;;
  vorschau) shift; exec $PY -m technoloop bauen projekt.json --vorschau 120 --ab 5:00 "$@" ;;
  bauen) shift; exec $PY -m technoloop bauen projekt.json "$@" ;;
  song) shift; exec $PY -m technoloop song-dazu projekt.json "$@" ;;
  keyframes) shift; exec $PY -m technoloop keyframes projekt.json "$@" ;;
  resolve) shift; exec $PY -m technoloop resolve projekt.json "$@" ;;
  demo) $PY -m technoloop demo demo && exec $PY -m technoloop bauen demo/projekt.json ;;
  *) echo "Benutzung: $0 setup|keyframes|szenen|vorschau|bauen|song|resolve|demo"; exit 1 ;;
esac
