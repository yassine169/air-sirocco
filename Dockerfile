# Image de base : Python 3.11 léger
FROM python:3.11-slim

# Dossier de travail dans le conteneur
WORKDIR /app

# On installe d'abord les dépendances (étape mise en cache par Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Puis on copie le code du projet
COPY . .

# Commande lancée au démarrage du conteneur
CMD ["sh", "run_pipeline.sh"]
