#!/bin/sh
set -e
# Affichage immédiat dans les logs Railway
echo "[start] Démarrage du conteneur..."
echo "[start] PORT=${PORT:-non défini}"
echo "[start] SUPABASE_URL: $(test -n "$SUPABASE_URL" && echo 'défini' || echo 'MANQUANT')"
echo "[start] SUPABASE_SERVICE_KEY: $(test -n "$SUPABASE_SERVICE_KEY" && echo 'défini' || echo 'MANQUANT')"
echo "[start] Lancement API + Scheduler..."
# Scheduler en arrière-plan, API au premier plan (stderr vers stdout pour voir les erreurs Python)
python src/scheduler/cron_jobs.py &
exec python src/api/server.py 2>&1
