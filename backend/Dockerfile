FROM python:3.12-slim

WORKDIR /app

# Installer les dépendances
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY app/ ./app/

# Créer un utilisateur non privilégié
RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app

USER appuser

# Exposer le port de l'API
EXPOSE 8000

# Démarrer FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
