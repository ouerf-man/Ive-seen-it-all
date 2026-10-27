#!/usr/bin/env bash
# Installs the /effect-name shortcut commands (/orbit, /paper-cut, ...) next to this skill.
# A folder that already exists and is not one of our shortcuts is left alone.
cd "$(dirname "$0")/.."
SKILLS="$(cd .. && pwd)"
for d in shortcuts/*/; do
  n=$(basename "$d"); t="$SKILLS/$n"
  if [ -e "$t" ] && ! grep -q "shortcut-of: studio-effects" "$t/SKILL.md" 2>/dev/null; then echo "skipped /$n (you already have a skill with that name)"; continue; fi
  mkdir -p "$t" && cp "$d/SKILL.md" "$t/SKILL.md"
done
echo "SHORTCUTS READY — restart Claude to use /orbit, /paper-cut ..."
