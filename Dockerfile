# ─────────────────────────────────────────────
# Dockerfile  (versión base)
# ─────────────────────────────────────────────

# Imagen base oficial de Python
FROM python:3.11-slim

# Metadata
LABEL maintainer="tu-email@ejemplo.com"
LABEL description="Instagram Video Downloader - versión base"

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivo de dependencias primero (mejor uso del cache)
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app.py .

# Exponer el puerto de la app
EXPOSE 5000

# Comando por defecto al iniciar el contenedor
CMD ["python", "app.py"]