# One-time setup for studio-effects on Windows (PowerShell). Safe to run again: prints READY when everything is in place.
$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')

if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) { Write-Output 'NEED_FFMPEG: winget install ffmpeg  (then open a new terminal)'; exit 1 }
if (-not (Get-Command npx -ErrorAction SilentlyContinue)) { Write-Output 'NEED_NODE: winget install OpenJS.NodeJS.LTS  (then open a new terminal)'; exit 1 }

$venvPy = '.venv\Scripts\python.exe'
$ok = $false
if (Test-Path $venvPy) { & $venvPy -c "import mediapipe, cv2, PIL, numpy" 2>$null; $ok = ($LASTEXITCODE -eq 0) }
if (-not $ok) {
  $py = $null
  foreach ($c in @('py -3.12', 'py -3.11', 'py -3.13', 'python')) {
    $parts = $c.Split(' ')
    try { & $parts[0] $parts[1..9] -c "import sys; sys.exit(0 if sys.version_info[:2] >= (3, 10) else 1)" 2>$null; if ($LASTEXITCODE -eq 0) { $py = $parts; break } } catch {}
  }
  if (-not $py) { Write-Output 'NEED_PYTHON: winget install Python.Python.3.12  (then open a new terminal)'; exit 1 }
  & $py[0] $py[1..9] -m venv .venv
  & $venvPy -m pip install -q --upgrade pip
  & $venvPy -m pip install -q -r setup\requirements.txt
}

New-Item -ItemType Directory -Force -Path models | Out-Null
$B = 'https://storage.googleapis.com/mediapipe-models'
$files = @{
  'face_landmarker.task' = "$B/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
  'hand_landmarker.task' = "$B/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
  'selfie_multiclass_256x256.tflite' = "$B/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite"
}
foreach ($k in $files.Keys) { if (-not (Test-Path "models\$k")) { Invoke-WebRequest -Uri $files[$k] -OutFile "models\$k" } }

& (Join-Path $PSScriptRoot 'shortcuts.ps1') | Out-Null
npx --yes hyperframes --version *> $null
if ($LASTEXITCODE -ne 0) { Write-Output 'NEED_HYPERFRAMES: npx hyperframes failed, check your internet and Node'; exit 1 }
& $venvPy -c "import mediapipe, cv2, PIL, numpy; print('READY')"
