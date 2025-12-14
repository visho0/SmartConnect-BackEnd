# 📋 Resumen Rápido: Despliegue AWS RDS + EC2

## 🎯 Pasos Principales

### 1️⃣ Configurar RDS (PostgreSQL)
- Crear instancia RDS PostgreSQL
- Anotar: endpoint, usuario, contraseña
- Configurar Security Group para permitir acceso desde EC2

### 2️⃣ Configurar EC2 (Ubuntu Server)
- Crear instancia EC2 Ubuntu 22.04
- Configurar Security Groups (SSH, HTTP, HTTPS)
- Conectar vía SSH

### 3️⃣ Preparar Proyecto
```bash
# En tu máquina local
# Actualizar requirements.txt (ya incluye psycopg2-binary y python-decouple)
# Subir código a EC2 (Git, SCP, o archivo comprimido)
```

### 4️⃣ Configurar EC2
```bash
# En EC2
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv postgresql-client nginx supervisor

# O usar el script
chmod +x deploy_scripts/setup_aws.sh
./deploy_scripts/setup_aws.sh
```

### 5️⃣ Desplegar Código
```bash
cd /var/www/smartconnect
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 6️⃣ Configurar Variables de Entorno
```bash
nano .env
```

Contenido `.env`:
```env
DEBUG=False
SECRET_KEY=generar-nueva-key
ALLOWED_HOSTS=tu-ip-ec2,tu-dominio.com
DB_NAME=smartconnect_db
DB_USER=smartconnect_admin
DB_PASSWORD=password-rds
DB_HOST=endpoint-rds.amazonaws.com
DB_PORT=5432
```

### 7️⃣ Configurar Base de Datos
```bash
python manage.py migrate
python manage.py create_initial_data
python manage.py collectstatic --noinput
```

### 8️⃣ Configurar Gunicorn + Supervisor
- Archivo `gunicorn_config.py` ya creado
- Configurar `/etc/supervisor/conf.d/smartconnect.conf`
- Ver DEPLOY_AWS.md para detalles

### 9️⃣ Configurar Nginx
- Configurar `/etc/nginx/sites-available/smartconnect`
- Ver DEPLOY_AWS.md para detalles

### 🔟 Probar
```bash
curl http://tu-ip-ec2/api/info/
```

## 📁 Archivos Importantes Creados

- ✅ `DEPLOY_AWS.md` - Guía completa detallada
- ✅ `gunicorn_config.py` - Configuración Gunicorn
- ✅ `.env.example` - Ejemplo de variables de entorno
- ✅ `.gitignore` - Para no subir archivos sensibles
- ✅ `deploy_scripts/` - Scripts auxiliares
- ✅ `settings.py` - Actualizado para usar variables de entorno

## 🔑 Información Necesaria

Antes de empezar, necesitas:
1. Endpoint de RDS (ej: `smartconnect-db.xxxxx.us-east-1.rds.amazonaws.com`)
2. Usuario y contraseña de RDS
3. IP pública de EC2
4. Archivo `.pem` para conectarte a EC2

## 💡 Tip Rápido

Para generar SECRET_KEY:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 📖 Documentación Completa

Ver `DEPLOY_AWS.md` para instrucciones detalladas paso a paso.

