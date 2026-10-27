# Installs the /effect-name shortcut commands (/orbit, /paper-cut, ...) next to this skill.
# A folder that already exists and is not one of our shortcuts is left alone.
Set-Location (Join-Path $PSScriptRoot '..')
$skills = Split-Path -Parent (Get-Location)
Get-ChildItem shortcuts -Directory | ForEach-Object {
  $t = Join-Path $skills $_.Name; $f = Join-Path $t 'SKILL.md'
  if ((Test-Path $t) -and -not ((Test-Path $f) -and (Select-String -Path $f -Pattern 'shortcut-of: studio-effects' -Quiet))) { Write-Output "skipped /$($_.Name) (you already have a skill with that name)"; return }
  New-Item -ItemType Directory -Force -Path $t | Out-Null
  Copy-Item (Join-Path $_.FullName 'SKILL.md') $f -Force
}
Write-Output 'SHORTCUTS READY - restart Claude to use /orbit, /paper-cut ...'
