#!/bin/zsh
cd "$(dirname "$0")"
rm -f .git/*.lock .git/*.stale* 2>/dev/null
git add -A
git commit -m "Update $(date +%d.%m.%Y_%H%M)"
git pull --rebase origin main
git push origin main
echo ""
echo "Fertig - in ca. 1 Minute live auf abu-tools.ch"
sleep 3
