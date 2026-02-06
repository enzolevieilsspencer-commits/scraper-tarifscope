# Image Python sur Debian (bookworm = apt pour install-deps)
FROM python:3.9-bookworm

WORKDIR /app

# Dépendances Python + Playwright
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Chromium + dépendances système en une commande (évite "missing dependencies")
RUN playwright install chromium --with-deps

COPY . .

# Pour voir les logs immédiatement (sinon buffer et on ne voit rien au démarrage)
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

# Scheduler en arrière-plan, API au premier plan (PID 1) pour que ses logs s'affichent
CMD ["sh", "-c", "python src/scheduler/cron_jobs.py & exec python src/api/server.py"]
