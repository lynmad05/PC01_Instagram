# 📥 Aplicación de Descarga de Videos de Instagram con Docker

## 📌 Descripción

Este proyecto consiste en una aplicación que permite descargar videos desde Instagram.
La aplicación ha sido contenerizada utilizando Docker, implementando tres versiones de Dockerfile:

* Dockerfile básico
* Dockerfile optimizado
* Dockerfile multistage

---

## 🚀 1. Clonar el repositorio

```bash
git clone https://github.com/lynmad05/PC01_Instagram.git
cd PC01_Instagram
```

---

## 🐳 2. Construir las imágenes Docker

### a) Versión base

```bash
docker build -t instagram-dl:v1.0 .
```

### b) Versión optimizada

```bash
docker build -f Dockerfile.optimizado -t instagram-dl:v1.1-alpine .
```

### c) Versión multistage

```bash
docker build -f Dockerfile.multistage -t instagram-dl:v1.2-multistage .
```

---

## 📊 3. Comparar tamaños de imágenes

```bash
docker images | grep instagram-dl
```

---

## ▶️ 4. Ejecutar el contenedor

```bash

### Versión base
docker run -d -p 5000:5000 --name instagram-app instagram-dl:v1.0

### Versión optimizada
docker run -d -p 5000:5000 --name instagram-app instagram-dl:v1.1-alpine

### Versión multistage
docker run -d -p 5000:5000 --name instagram-app instagram-dl:v1.2-multistage
```

📌 Nota:
Si el puerto 5000 está en uso, puedes cambiarlo:

```bash
docker run -d -p 5001:5000 --name instagram-app instagram-dl:v1.0
```

---

## 🔍 5. Verificar ejecución

```bash
docker ps
docker logs instagram-app
```

---

## 🌐 6. Probar la aplicación

Abrir en el navegador:

👉 http://localhost:5000

(o si cambiaste el puerto: http://localhost:5001)

---

## Problemas comunes

### Puerto en uso

Error:

```
port is already allocated
```

Solución: usar otro puerto o detener el contenedor en uso.

---

### Nombre de contenedor en uso

Error:

```
container name is already in use
```

Solución:

```bash
docker rm -f instagram-app
```

---
## Captura de la aplicación para descargar

<img width="1844" height="854" alt="image" src="https://github.com/user-attachments/assets/bd8e64a3-c4a9-4def-b150-9decc8282c5e" />
<img width="1892" height="867" alt="image" src="https://github.com/user-attachments/assets/c542f887-bebb-4303-abfe-0bf11602527a" />


## 🧠 Conclusiones

* Se logró desarrollar una aplicación funcional para la descarga de videos de Instagram utilizando Docker.
* Se aplicaron diferentes estrategias de construcción de imágenes (básica, optimizada y multistage).
* Se comprendió la importancia del manejo de contenedores, puertos y optimización de imágenes en Docker.

---

## Autora

Ailyn Medina Mallqui - https://github.com/lynmad05 
