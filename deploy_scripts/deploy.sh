#!/bin/bash
# Script de despliegue - ejecutar después de actualizar código
# Ejecutar desde /var/www/smartconnect

echo "🚀 Desplegando SmartConnect..."

# Activar entorno virtual
source venv/bin/activate

# Instalar/actualizar dependencias
echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Ejecutar migraciones
echo "🔄 Ejecutando migraciones..."
python manage.py migrate

# Recolectar archivos estáticos
echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Reiniciar aplicación
echo "🔄 Reiniciando aplicación..."
sudo supervisorctl restart smartconnect

# Verificar estado
echo "✅ Verificando estado..."
sudo supervisorctl status smartconnect

echo "✅ Despliegue completado!"

