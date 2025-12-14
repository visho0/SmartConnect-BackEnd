# Guía de Despliegue en AWS - SmartConnect API
Resumen rápido al reconectarte
Cada vez que te reconectas, ejecuta estos comandos:
cd /var/www/smartconnectsource venv/bin/activate
Luego puedes continuar con los comandos de Django/Python.

Esta guía te ayudará a desplegar la API SmartConnect en AWS usando EC2 y RDS.

## 📋 Requisitos Previos

- Cuenta de AWS activa
- Acceso a AWS Console
- Conocimientos básicos de Linux/terminal
- Tu proyecto funcionando localmente

## 🗂️ Arquitectura Propuesta

```
Internet → EC2 (Aplicación Django) → RDS (Base de datos PostgreSQL)
```

## 📝 Paso 1: Configurar RDS (Base de Datos)

### 1.1 Crear Instancia RDS PostgreSQL

1. **Accede a AWS Console** → RDS → Databases → Create database

2. **Configuración:**
   - **Engine type**: PostgreSQL
   - **Version**: PostgreSQL 15.x o superior
   - **Template**: Free tier (para pruebas) o Production
   - **DB instance identifier**: `smartconnect-db`
   - **Master username**: `connect_admin` (guarda este nombre)
   - **Master password**: Genera una contraseña segura `contradb123.` (guárdala)
   - **Instance class**: `db.t3.micro` (free tier) o `db.t3.small` (producción)
   - **Storage**: 20 GB inicial
   - **Storage autoscaling**: Habilitado (opcional)

3. **Connectivity:**
   - **VPC**: Usa la VPC por defecto o crea una nueva Default VPC (vpc-05dd42e64807ad3b0)
   - **Subnet group**: Por defecto
   - **Public access**: **NO** (más seguro)
   - **VPC security group**: Crea uno nuevo llamado `rds-sg1`
   - **Database port**: 5432 (por defecto)

4. **Database authentication**: Password authentication

5. **Initial database name**: `smartconnect_db`

6. **Backup**: Habilitar backups automáticos

7. **Click "Create database"**

### 1.2 Configurar Security Group de RDS

1. Ve a **EC2 Console** → **Security Groups**
2. Busca el grupo `rds-sg1` que creaste
3. **Edit inbound rules:**
   - **Type**: PostgreSQL
   - **Source**: Selecciona el Security Group de tu EC2 (lo crearemos después)
   - **Description**: "Acceso desde EC2"

## 📝 Paso 2: Configurar EC2 (Servidor)

### 2.1 Crear Instancia EC2

1. **Accede a EC2 Console** → **Launch Instance**

2. **Name**: `smartconnect-api-server`

3. **AMI**: Ubuntu Server 22.04 LTS (Free tier eligible)

4. **Instance type**: `t2.micro` (free tier) o `t2.small` (producción)

5. **Key pair**: Crea uno nuevo o usa existente (descarga el `.pem`)

6. **Network settings:**
   - **Security group**: Crea nuevo → `smartconnect-ec2-sg`
   - **Allow SSH**: Desde tu IP
   - **Allow HTTP**: Desde cualquier lugar (0.0.0.0/0)
   - **Allow HTTPS**: Desde cualquier lugar (0.0.0.0/0)

7. **Configure storage**: 20 GB mínimo

8. **Launch instance**

### 2.2 Configurar Security Group de EC2

1. Ve a **EC2 Console** → **Security Groups**
2. Selecciona `smartconnect-ec2-sg`
3. **Edit inbound rules:**
   - **SSH (22)**: Tu IP personal
   - **HTTP (80)**: 0.0.0.0/0
   - **HTTPS (443)**: 0.0.0.0/0
   - **Custom TCP (8000)**: 0.0.0.0/0 (para testing)

4. **Edit outbound rules:**
   - **All traffic**: 0.0.0.0/0

## 📝 Paso 3: Preparar el Proyecto

### 3.1 Crear archivo `.env.example`

Crea un archivo `.env.example` en la raíz del proyecto:

```env
# Django Settings
DEBUG=False
SECRET_KEY=tu-secret-key-super-segura-aqui-generar-nueva
ALLOWED_HOSTS=tu-ec2-public-ip,tu-dominio.com

# Database (RDS)
DB_NAME=smartconnect_db
DB_USER=smartconnect_admin
DB_PASSWORD=tu-password-rds
DB_HOST=smartconnect-db.xxxxxxxxxx.us-east-1.rds.amazonaws.com
DB_PORT=5432

# AWS Settings
AWS_REGION=us-east-1
```

### 3.2 Actualizar `requirements.txt`

Asegúrate de que incluye `psycopg2-binary` para PostgreSQL:

```txt
Django==6.0
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1
django-cors-headers==4.3.1
Pillow==10.2.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
python-decouple==3.8
```

### 3.3 Actualizar `settings.py` para producción

El archivo `settings.py` debe usar variables de entorno. Ya está parcialmente configurado, pero asegúrate de que tenga:

```python
import os
from decouple import config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-bruzbdm$qvu#tho-_ujwy0=7@#6^ixc!&8_ah^nggc$6*(0juu')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

## 📝 Paso 4: Conectar a EC2 y Configurar Servidor

### 4.1 Conectar vía SSH

```bash
ssh -i claves_connect.pem ubuntu@98.81.21.18
```

### 4.2 Actualizar sistema

```bash
sudo apt update
sudo apt upgrade -y
```

### 4.3 Instalar dependencias del sistema

```bash
sudo apt install -y python3-pip python3-venv postgresql-client nginx supervisor
```

### 4.4 Instalar Node.js (opcional, para gestión de procesos)

```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

## 📝 Paso 5: Desplegar Código en EC2

### 5.1 Crear directorio para la aplicación

```bash
sudo mkdir -p /var/www/smartconnect
sudo chown ubuntu:ubuntu /var/www/smartconnect
cd /var/www/smartconnect
```

### 5.2 Subir código (3 opciones)

**Opción A: Git (Recomendado)**
```bash
# Si tu proyecto está en GitHub/GitLab
git clone https://github.com/visho0/SmartConnect-BackEnd.git
```

**Opción B: SCP desde tu máquina local**
```bash
# Desde tu máquina local (en otra terminal)
scp -i tu-llave.pem -r . ubuntu@tu-ec2-ip:/var/www/smartconnect/
```

**Opción C: Crear archivo comprimido**
```bash
# Desde tu máquina local
tar -czf smartconnect.tar.gz .
scp -i tu-llave.pem smartconnect.tar.gz ubuntu@tu-ec2-ip:/tmp/
# En EC2
cd /var/www/smartconnect
tar -xzf /tmp/smartconnect.tar.gz
```

### 5.3 Crear entorno virtual

```bash
cd /var/www/smartconnect
python3 -m venv venv
source venv/bin/activate
```

### 5.4 Instalar dependencias Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5.5 Crear archivo `.env` en EC2

```bash
nano .env
```

Pega el contenido (ajusta los valores):

```env
DEBUG=False
SECRET_KEY=d9@zdj7c+8ez)pu!%q565+rcw-6-#*q+m=)5by^lf34qq1d42g
ALLOWED_HOSTS=ec2-98-81-21-18.compute-1.amazonaws.com

DB_NAME=smartconnect_db
DB_USER=connect_admin
DB_PASSWORD=contradb123.
DB_HOST=smartconnect-db.c9uk5jvpenlv.us-east-1.rds.amazonaws.com
DB_PORT=5432
```

**Para generar SECRET_KEY:**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Para obtener el endpoint de RDS:**
Ve a RDS Console → Tu base de datos → Connectivity & security → Endpoint

### 5.6 Actualizar settings.py para usar variables de entorno

Asegúrate de que `settings.py` tenga las importaciones correctas.

### 5.7 Ejecutar migraciones

```bash
python manage.py migrate
```

### 5.8 Crear datos iniciales

```bash
python manage.py create_initial_data
```

### 5.9 Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 5.10 Recolectar archivos estáticos

```bash
python manage.py collectstatic --noinput
```

## 📝 Paso 6: Configurar Gunicorn

### 6.1 Crear archivo de configuración Gunicorn

```bash
nano /var/www/smartconnect/gunicorn_config.py
```

Contenido:

```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
user = "ubuntu"
group = "ubuntu"
pidfile = "/var/run/gunicorn/smartconnect.pid"
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"
```

### 6.2 Crear directorios de logs y PID

```bash
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/run/gunicorn
sudo chown ubuntu:ubuntu /var/log/gunicorn
sudo chown ubuntu:ubuntu /var/run/gunicorn
```

### 6.3 Probar Gunicorn manualmente

```bash
cd /var/www/smartconnect
source venv/bin/activate
gunicorn smartconnect.wsgi:application --config gunicorn_config.py
```

Si funciona, presiona `Ctrl+C` para detenerlo.

## 📝 Paso 7: Configurar Supervisor (Gestión de procesos)

### 7.1 Crear archivo de configuración

```bash
sudo nano /etc/supervisor/conf.d/smartconnect.conf
```

Contenido:

```ini
[program:smartconnect]
command=/var/www/smartconnect/venv/bin/gunicorn smartconnect.wsgi:application --config /var/www/smartconnect/gunicorn_config.py
directory=/var/www/smartconnect
user=ubuntu
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/gunicorn/supervisor.log
environment=PATH="/var/www/smartconnect/venv/bin"
```

### 7.2 Configurar Supervisor

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start smartconnect
sudo supervisorctl status smartconnect
```

## 📝 Paso 8: Configurar Nginx (Web Server)

### 8.1 Crear configuración de Nginx

```bash
sudo nano /etc/nginx/sites-available/smartconnect
```

Contenido:

```nginx
server {
    listen 80;
    server_name ec2-54-225-212-23.compute-1.amazonaws.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    location /static/ {
        alias /var/www/smartconnect/staticfiles/;
    }

    location /media/ {
        alias /var/www/smartconnect/media/;
    }
}
```

### 8.2 Habilitar sitio

```bash
sudo ln -s /etc/nginx/sites-available/smartconnect /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx
```

## 📝 Paso 9: Configurar Firewall (Security Groups)

### 9.1 En AWS Console

Asegúrate de que el Security Group de RDS permita conexiones desde el Security Group de EC2:

1. Ve a **RDS** → Tu base de datos → **Connectivity & security**
2. Click en el Security Group
3. **Edit inbound rules**
4. Agrega regla:
   - Type: PostgreSQL
   - Source: Selecciona el Security Group de EC2
   - Save

## 📝 Paso 10: Probar la API

### 10.1 Probar endpoint público

```bash
curl http://54.225.212.23/api/info/
```

### 10.2 Probar login

```bash
curl -X POST http://54.225.212.23/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'


  
  # ignorar//////
  #Guarda el token en una variable (reemplaza con tu token real)
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY1ODI5OTcyLCJpYXQiOjE3NjU3NDM1NzIsImp0aSI6IjdhMGEzYTlkODNkZTRmOWY5YzA1YTQ0MWVmNTYyY2MyIiwidXNlcl9pZCI6MSwicm9sIjoiYWRtaW4iLCJ1c2VybmFtZSI6ImFkbWluIn0.lpR1pScyVUcEp3yZCWeYyJ4d3P_hyBXvPAzQpek88TU"

# Prueba un endpoint protegido (por ejemplo, listar departamentos)
curl http://54.225.212.23/api/departamentos/ \
  -H "Authorization: Bearer $TOKEN"
```

### 10.3 Probar endpoint protegido

```bash
# Primero obtén el token (guarda el valor de "access")
TOKEN="tu-token-aqui"

curl http://tu-ec2-public-ip/api/departamentos/ \
  -H "Authorization: Bearer $TOKEN"
```

## 📝 Paso 11: Configurar Dominio (Opcional)

### 11.1 Obtener dominio

Compra un dominio en Route 53 o cualquier proveedor.

### 11.2 Configurar DNS

Crea un registro A que apunte a la IP pública de tu EC2.

### 11.3 Actualizar ALLOWED_HOSTS

Edita `.env` y agrega tu dominio:

```env
ALLOWED_HOSTS=tu-ec2-ip,tu-dominio.com,www.tu-dominio.com
```

Reinicia Gunicorn:

```bash
sudo supervisorctl restart smartconnect
```

### 11.4 Configurar SSL con Let's Encrypt (Opcional)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

## 🔒 Seguridad Adicional

### Variables de entorno

Nunca subas el archivo `.env` a Git. Agrega a `.gitignore`:

```
.env
*.env
```

### Actualizar Secret Key

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Firewall local

```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## 🐛 Troubleshooting

### Error 404 de Nginx (Ruta no encontrada)

Si obtienes un error 404 de nginx al acceder a `/api/info/`, sigue estos pasos:

**1. Verificar que Gunicorn está corriendo:**
```bash
sudo supervisorctl status smartconnect
# Debe mostrar: smartconnect RUNNING pid XXXX
```

Si no está corriendo:
```bash
sudo supervisorctl start smartconnect
sudo supervisorctl status smartconnect
```

**2. Verificar que Gunicorn está escuchando en el puerto 8000:**
```bash
sudo netstat -tlnp | grep 8000
# O usar:
sudo ss -tlnp | grep 8000
# Debe mostrar que python/gunicorn está escuchando en 127.0.0.1:8000
```

**3. Probar Gunicorn directamente (desde dentro de EC2):**
```bash
curl http://127.0.0.1:8000/api/info/
# Si esto funciona, el problema es nginx. Si no funciona, el problema es Gunicorn/Django.
```

**4. Verificar configuración de Nginx:**
```bash
# Verificar que el sitio está habilitado
ls -la /etc/nginx/sites-enabled/ | grep smartconnect

# Verificar sintaxis de nginx
sudo nginx -t

# Ver la configuración actual
sudo cat /etc/nginx/sites-available/smartconnect
```

**5. Verificar que el server_name en nginx coincide:**
```bash
# Obtener el hostname público de tu instancia
curl http://169.254.169.254/latest/meta-data/public-hostname

# Asegúrate de que el server_name en /etc/nginx/sites-available/smartconnect
# coincida con este hostname, o usa _ (guion bajo) para aceptar cualquier dominio:
# server_name _;
```

**6. Si el server_name no coincide, actualízalo:**
```bash
sudo nano /etc/nginx/sites-available/smartconnect
# Cambia server_name a _ o al hostname correcto
sudo nginx -t
sudo systemctl restart nginx
```

**7. Ver logs en tiempo real mientras haces la petición:**
```bash
# Terminal 1: Logs de nginx
sudo tail -f /var/log/nginx/error.log

# Terminal 2: Logs de gunicorn
tail -f /var/log/gunicorn/error.log

# Terminal 3: Hacer la petición
curl http://TU-IP/api/info/
```

### Ver logs de Gunicorn

```bash
tail -f /var/log/gunicorn/error.log
tail -f /var/log/gunicorn/access.log
```

### Ver logs de Supervisor

```bash
sudo supervisorctl tail -f smartconnect
```

### Ver logs de Nginx

```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Verificar estado de servicios

```bash
sudo supervisorctl status
sudo systemctl status nginx
```

### Reiniciar servicios

```bash
sudo supervisorctl restart smartconnect
sudo systemctl restart nginx
```

### Probar conexión a RDS desde EC2

```bash
psql -h smartconnect-db.xxxxx.rds.amazonaws.com -U smartconnect_admin -d smartconnect_db
```

## 📊 Monitoreo y Mantenimiento

### Actualizar código

```bash
cd /var/www/smartconnect
source venv/bin/activate
git pull  # o subir nuevo código
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart smartconnect
```

### Backup de base de datos

Configura backups automáticos en RDS Console o crea snapshots manuales.

### Escalado

- **EC2**: Cambia el instance type en EC2 Console
- **RDS**: Modifica el instance class en RDS Console
- **Load Balancing**: Configura Application Load Balancer frente a múltiples EC2

## 💰 Costos Estimados (Free Tier)

- **EC2 t2.micro**: Gratis por 12 meses (750 horas/mes)
- **RDS db.t3.micro**: Gratis por 12 meses (750 horas/mes)
- **Datos transferidos**: 1GB/mes gratis

**Después del free tier:**
- EC2 t2.micro: ~$8-10/mes
- RDS db.t3.micro: ~$15-20/mes
- Total: ~$25-30/mes

## ✅ Checklist de Despliegue

- [ ] RDS configurado y accesible desde EC2
- [ ] EC2 creado con Security Groups correctos
- [ ] Código subido a EC2
- [ ] Variables de entorno configuradas (.env)
- [ ] Dependencias instaladas
- [ ] Migraciones ejecutadas
- [ ] Datos iniciales creados
- [ ] Gunicorn funcionando
- [ ] Supervisor configurado
- [ ] Nginx configurado
- [ ] API responde correctamente
- [ ] SSL configurado (si usas dominio)
- [ ] Backups configurados
- [ ] Monitoreo configurado

¡Felicitaciones! Tu API está desplegada en AWS. 🎉

