# Dockerfile per il provisioning su Raspberry Pi / gateway IoT
# Build: docker build -t auto-provisioner-mesh-iot .
# Run:   docker run --env-file .env --network host auto-provisioner-mesh-iot

FROM python:3.12-slim

WORKDIR /app

# Installa dipendenze di sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Installa Tailscale
RUN curl -fsSL https://tailscale.com/install.sh | sh

# Installa dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice sorgente
COPY src/ ./src/
COPY examples/ ./examples/

# Variabili d'ambiente di default (sovrascrivibili)
ENV TAILSCALE_AUTH_KEY=""
ENV TAILSCALE_API_TOKEN=""
ENV TAILSCALE_TAILNET=""

ENTRYPOINT ["python", "src/provisioner.py"]
CMD ["--config", "examples/devices.yaml.example"]
