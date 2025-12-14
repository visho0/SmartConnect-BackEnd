#!/bin/bash
# Script de configuración inicial para AWS EC2
# Ejecutar en el servidor EC2 después de conectarse vía SSH

echo "🚀 Iniciando configuración de SmartConnect en AWS..."

# Actualizar sistema
echo "📦 Actualizando sistema..."
sudo apt update
sudo apt upgrade -y

# Instalar dependencias del sistema
echo "📦 Instalando dependencias del sistema..."
sudo apt install -y python3-pip python3-venv postgresql-client nginx supervisor

# Crear directorio para la aplicación
echo "📁 Creando directorios..."
sudo mkdir -p /var/www/smartconnect
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/run/gunicorn
sudo chown -R ubuntu:ubuntu /var/www/smartconnect
sudo chown -R ubuntu:ubuntu /var/log/gunicorn
sudo chown -R ubuntu:ubuntu /var/run/gunicorn

echo "✅ Configuración inicial completada!"
echo "📝 Próximos pasos:"
echo "   1. Subir código a /var/www/smartconnect"
echo "   2. Crear entorno virtual: python3 -m venv venv"
echo "   3. Instalar dependencias: pip install -r requirements.txt"
echo "   4. Crear archivo .env con las variables de entorno"
echo "   5. Ejecutar migraciones: python manage.py migrate"
echo "   6. Configurar Gunicorn y Supervisor"
echo "   7. Configurar Nginx"

