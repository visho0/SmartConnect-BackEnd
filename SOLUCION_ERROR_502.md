# 🔧 Solución al Error 502 Bad Gateway

## ¿Qué significa el error 502?

El error **502 Bad Gateway** significa que **Nginx está funcionando**, pero **no puede comunicarse con Gunicorn** (el servidor Django). Es como si Nginx fuera el portero de un edificio, pero el ascensor (Gunicorn) no está funcionando.

---

## 🔍 Diagnóstico Paso a Paso

### Paso 1: Verificar que Gunicorn está corriendo

Conéctate a tu servidor EC2 y ejecuta:

```bash
sudo supervisorctl status smartconnect
```

**Resultado esperado:**
```
smartconnect    RUNNING    pid 12345, uptime 0:05:23
```

**Si dice `STOPPED` o `FATAL`:**
```bash
# Iniciar Gunicorn
sudo supervisorctl start smartconnect

# Ver logs para entender el error
sudo supervisorctl tail -f smartconnect
```

**Si dice que no existe:**
```bash
# Reconfigurar Supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start smartconnect
```

---

### Paso 2: Verificar que Gunicorn está escuchando en el puerto 8000

```bash
sudo netstat -tlnp | grep 8000
# O usar:
sudo ss -tlnp | grep 8000
```

**Resultado esperado:**
```
tcp    0    0 127.0.0.1:8000    0.0.0.0:*    LISTEN    12345/python
```

**Si no muestra nada:**
- Gunicorn no está corriendo o no está escuchando en el puerto correcto
- Revisa el archivo `gunicorn_config.py` y asegúrate de que `bind = "127.0.0.1:8000"`

---

### Paso 3: Probar Gunicorn directamente (desde dentro del servidor)

```bash
curl http://127.0.0.1:8000/api/info/
```

**Si funciona:**
- ✅ Gunicorn está bien
- ❌ El problema es la configuración de Nginx

**Si NO funciona:**
- ❌ El problema es Gunicorn/Django
- Revisa los logs: `tail -f /var/log/gunicorn/error.log`

---

### Paso 4: Verificar configuración de Nginx

```bash
# Ver la configuración actual
sudo cat /etc/nginx/sites-available/smartconnect
```

**Configuración correcta debe tener:**

```nginx
server {
    listen 80;
    server_name _;  # o tu dominio/IP

    location / {
        proxy_pass http://127.0.0.1:8000;  # ← ESTO ES CRÍTICO
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

**⚠️ PROBLEMA COMÚN:** Si falta la línea `proxy_pass http://127.0.0.1:8000;`, Nginx no sabrá a dónde enviar las peticiones.

---

### Paso 5: Verificar sintaxis de Nginx

```bash
sudo nginx -t
```

**Resultado esperado:**
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

**Si hay errores:**
- Corrígelos antes de continuar
- Edita el archivo: `sudo nano /etc/nginx/sites-available/smartconnect`

---

### Paso 6: Verificar que el sitio está habilitado

```bash
ls -la /etc/nginx/sites-enabled/ | grep smartconnect
```

**Debe mostrar un enlace simbólico:**
```
lrwxrwxrwx ... smartconnect -> /etc/nginx/sites-available/smartconnect
```

**Si no existe:**
```bash
sudo ln -s /etc/nginx/sites-available/smartconnect /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

### Paso 7: Verificar logs en tiempo real

Abre **3 terminales** (o 3 pestañas) en tu servidor:

**Terminal 1 - Logs de Nginx:**
```bash
sudo tail -f /var/log/nginx/error.log
```

**Terminal 2 - Logs de Gunicorn:**
```bash
tail -f /var/log/gunicorn/error.log
```

**Terminal 3 - Hacer petición:**
```bash
curl http://TU-IP-PUBLICA/api/info/
```

Observa qué errores aparecen en las terminales 1 y 2.

---

## 🛠️ Soluciones Comunes

### Solución 1: Gunicorn no está corriendo

```bash
# Verificar estado
sudo supervisorctl status smartconnect

# Si está detenido, iniciarlo
sudo supervisorctl start smartconnect

# Si no existe, recrearlo
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start smartconnect

# Verificar que está corriendo
sudo supervisorctl status smartconnect
```

---

### Solución 2: Falta `proxy_pass` en Nginx

Edita la configuración:

```bash
sudo nano /etc/nginx/sites-available/smartconnect
```

Asegúrate de que dentro de `location / {` esté:

```nginx
location / {
    proxy_pass http://127.0.0.1:8000;  # ← ESTA LÍNEA ES OBLIGATORIA
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_redirect off;
}
```

Luego:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

---

### Solución 3: Gunicorn está escuchando en puerto incorrecto

Verifica `gunicorn_config.py`:

```bash
cat /var/www/smartconnect/gunicorn_config.py
```

Debe tener:
```python
bind = "127.0.0.1:8000"  # ← Debe ser 127.0.0.1:8000
```

Si está diferente, edítalo:
```bash
nano /var/www/smartconnect/gunicorn_config.py
```

Luego reinicia:
```bash
sudo supervisorctl restart smartconnect
```

---

### Solución 4: Problema con permisos o usuario

Verifica que Gunicorn puede ejecutarse:

```bash
# Verificar usuario en gunicorn_config.py
cat /var/www/smartconnect/gunicorn_config.py | grep user

# Debe ser: user = "ubuntu" (o el usuario que creaste)
```

Si el usuario es incorrecto, edítalo y reinicia:
```bash
sudo supervisorctl restart smartconnect
```

---

### Solución 5: Error en la aplicación Django

Si Gunicorn se inicia pero luego se detiene, revisa los logs:

```bash
tail -50 /var/log/gunicorn/error.log
```

**Errores comunes:**
- **Base de datos no conecta:** Verifica variables de entorno en `.env`
- **Migraciones pendientes:** `python manage.py migrate`
- **Archivos estáticos:** `python manage.py collectstatic --noinput`
- **Import errors:** Verifica que todas las dependencias están instaladas

---

### Solución 6: `server_name` incorrecto en Nginx

Si estás accediendo por IP pero el `server_name` tiene un dominio:

```bash
sudo nano /etc/nginx/sites-available/smartconnect
```

Cambia:
```nginx
server_name _;  # Acepta cualquier dominio/IP
```

O usa tu IP específica:
```nginx
server_name TU-IP-PUBLICA;
```

Luego:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔄 Reiniciar Todo (Último Recurso)

Si nada funciona, reinicia todos los servicios:

```bash
# Detener todo
sudo supervisorctl stop smartconnect
sudo systemctl stop nginx

# Iniciar Gunicorn
sudo supervisorctl start smartconnect
sudo supervisorctl status smartconnect

# Iniciar Nginx
sudo systemctl start nginx
sudo systemctl status nginx

# Verificar que ambos están corriendo
sudo supervisorctl status
sudo systemctl status nginx
```

---

## ✅ Verificación Final

Después de aplicar las soluciones, verifica:

```bash
# 1. Gunicorn corriendo
sudo supervisorctl status smartconnect
# Debe decir: RUNNING

# 2. Gunicorn escuchando
sudo ss -tlnp | grep 8000
# Debe mostrar: 127.0.0.1:8000

# 3. Nginx corriendo
sudo systemctl status nginx
# Debe decir: active (running)

# 4. Probar desde el servidor
curl http://127.0.0.1:8000/api/info/
# Debe devolver JSON con información

# 5. Probar desde fuera (reemplaza con tu IP)
curl http://TU-IP-PUBLICA/api/info/
# Debe devolver el mismo JSON
```

---

## 📋 Checklist Rápido

- [ ] Gunicorn está corriendo (`sudo supervisorctl status`)
- [ ] Gunicorn escucha en `127.0.0.1:8000` (`sudo ss -tlnp | grep 8000`)
- [ ] Nginx tiene `proxy_pass http://127.0.0.1:8000;` en la configuración
- [ ] El sitio está habilitado (`ls /etc/nginx/sites-enabled/`)
- [ ] Sintaxis de Nginx es correcta (`sudo nginx -t`)
- [ ] Nginx está corriendo (`sudo systemctl status nginx`)
- [ ] `server_name` acepta tu IP o dominio
- [ ] No hay errores en los logs

---

## 🆘 Si Nada Funciona

1. **Revisa todos los logs:**
   ```bash
   sudo tail -100 /var/log/nginx/error.log
   tail -100 /var/log/gunicorn/error.log
   sudo supervisorctl tail -100 smartconnect
   ```

2. **Prueba Gunicorn manualmente:**
   ```bash
   cd /var/www/smartconnect
   source venv/bin/activate
   gunicorn smartconnect.wsgi:application --bind 127.0.0.1:8000
   ```
   Si funciona manualmente, el problema es Supervisor.

3. **Verifica variables de entorno:**
   ```bash
   cat /var/www/smartconnect/.env
   ```

4. **Revisa la configuración completa:**
   ```bash
   sudo cat /etc/nginx/sites-available/smartconnect
   cat /var/www/smartconnect/gunicorn_config.py
   cat /etc/supervisor/conf.d/smartconnect.conf
   ```

---

## 💡 Causa Más Común

**En el 90% de los casos, el error 502 se debe a:**

1. **Gunicorn no está corriendo** → Solución: `sudo supervisorctl start smartconnect`
2. **Falta `proxy_pass` en Nginx** → Solución: Agregar la línea en la configuración
3. **Gunicorn escucha en puerto diferente** → Solución: Verificar `gunicorn_config.py`

¡Empieza por verificar estos 3 puntos y probablemente solucionarás el problema! 🚀

