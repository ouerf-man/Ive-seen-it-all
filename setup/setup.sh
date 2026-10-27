#!/usr/bin/env bash
# One-time setup for studio-effects on Mac (and Linux). Safe to run again: prints READY when everything is in place.
set -e
cd "$(dirname "$0")/.."

command -v ffmpeg >/dev/null 2>&1 && command -v ffprobe >/dev/null 2>&1 || { echo "NEED_FFMPEG: brew install ffmpeg"; exit 1; }
command -v npx >/dev/null 2>&1 || { echo "NEED_NODE: brew install node"; exit 1; }

if ! { [ -x .venv/bin/python ] && .venv/bin/python -c "import mediapipe, cv2, PIL, numpy" 2>/dev/null; }; then
  PY=""
  for v in python3.12 python3.11 python3.13 python3.10 python3; do
    if command -v "$v" >/dev/null 2>&1 && "$v" -c 'import sys; sys.exit(0 if sys.version_info[:2] >= (3, 10) else 1)' 2>/dev/null; then PY="$v"; break; fi
  done
  [ -n "$PY" ] || { echo "NEED_PYTHON: brew install python@3.12"; exit 1; }
  "$PY" -m venv .venv
  .venv/bin/python -m pip install -q --upgrade pip
  .venv/bin/python -m pip install -q -r setup/requirements.txt
fi

mkdir -p models
B=https://storage.googleapis.com/mediapipe-models
[ -s models/face_landmarker.task ] || curl -sSfL -o models/face_landmarker.task $B/face_landmarker/face_landmarker/float16/1/face_landmarker.task
[ -s models/hand_landmarker.task ] || curl -sSfL -o models/hand_landmarker.task $B/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
[ -s models/selfie_multiclass_256x256.tflite ] || curl -sSfL -o models/selfie_multiclass_256x256.tflite $B/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite

bash setup/shortcuts.sh >/dev/null 2>&1 || true
npx --yes hyperframes --version >/dev/null 2>&1 || { echo "NEED_HYPERFRAMES: npx hyperframes failed, check your internet and Node"; exit 1; }
.venv/bin/python -c "import mediapipe, cv2, PIL, numpy; print('READY')"
