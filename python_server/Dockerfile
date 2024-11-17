# Użyj oficjalnego obrazu Pythona jako obrazu bazowego
FROM python:3.9-slim

# Ustaw katalog roboczy w kontenerze
WORKDIR /usr/src/app

# Skopiuj plik server.py do kontenera
COPY server.py .

# Skopiuj plik requirements.txt, jeśli masz ten plik
COPY requirements.txt .

RUN apt-get update && apt-get install -y \
build-essential \
libpq-dev \
&& rm -rf /var/lib/apt/lists/*

# Zainstaluj wymagane zależności
RUN pip install --no-cache-dir -r requirements.txt



# Otwórz port 8000, na którym działa serwer Python
EXPOSE 8000

# Uruchom skrypt serwera
CMD ["python", "./server.py"]
