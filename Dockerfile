# Image Python sur Debian (bookworm = apt pour install-deps)
FROM python:3.9-bookworm

WORKDIR /app

# Dépendances Python + Playwright
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Chromium + dépendances système en une commande (évite "missing dependencies")
RUN playwright install chromium --with-deps

COPY . .

# Port exposé (Railway injecte PORT)
ENV PORT=8080
EXPOSE $PORT

CMD python src/scheduler/cron_jobs.py & python src/api/server.py
