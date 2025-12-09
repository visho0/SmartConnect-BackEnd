# SmartConnect Backend API

API RESTful desarrollada con Django Rest Framework para sistema de control de acceso inteligente con sensores RFID.

## 📋 Características Implementadas

- ✅ Autenticación JWT (JSON Web Tokens)
- ✅ Modelos: Usuario, Departamento, Sensor, Barrera, Evento
- ✅ CRUD completo para todas las entidades
- ✅ Permisos personalizados (Admin CRUD total, Operador solo lectura)
- ✅ Validaciones de datos
- ✅ Manejo profesional de errores (400, 401, 403, 404, 500)
- ✅ Endpoint de información del proyecto `/api/info/`
- ✅ Endpoint para simular intentos de acceso desde sensores
- ✅ Configuración lista para despliegue en AWS

## 🚀 Instrucciones de Instalación y Configuración

### Paso 1: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 2: Ejecutar migraciones

Primero, elimina la base de datos antigua si existe (ya que cambiamos el modelo de Usuario):

```bash
# Si existe db.sqlite3, elimínalo
del db.sqlite3  # Windows
# o
rm db.sqlite3  # Linux/Mac
```

Luego crea las migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Paso 3: Crear datos iniciales

Ejecuta el comando personalizado para crear usuarios y datos iniciales:

```bash
python manage.py create_initial_data
```

Esto creará:
- Usuario admin: `admin` / contraseña: `admin123`
- Usuario operador: `operador` / contraseña: `operador123`
- Departamento "Recepción"
- Barrera "Barrera Principal"

### Paso 4: Crear superusuario (opcional, para Django Admin)

```bash
python manage.py createsuperuser
```

### Paso 5: Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

La API estará disponible en: `http://localhost:8000/api/`

## 📚 Endpoints Disponibles

### Información del Proyecto (Público)
- `GET /api/info/` - Información del proyecto (no requiere autenticación)

### Autenticación
- `POST /api/token/` - Obtener token JWT (login)
- `POST /api/token/refresh/` - Refrescar token JWT

**Ejemplo de login:**
```json
POST /api/token/
{
  "username": "admin",
  "password": "admin123"
}

Respuesta:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Usuarios (Solo Admin)
- `GET /api/usuarios/` - Listar usuarios
- `GET /api/usuarios/{id}/` - Detalle de usuario
- `POST /api/usuarios/` - Crear usuario
- `PUT /api/usuarios/{id}/` - Actualizar usuario completo
- `PATCH /api/usuarios/{id}/` - Actualizar usuario parcial
- `DELETE /api/usuarios/{id}/` - Eliminar usuario
- `GET /api/usuarios/me/` - Información del usuario autenticado

### Departamentos
- `GET /api/departamentos/` - Listar departamentos (Autenticado)
- `GET /api/departamentos/{id}/` - Detalle de departamento (Autenticado)
- `POST /api/departamentos/` - Crear departamento (Admin)
- `PUT /api/departamentos/{id}/` - Actualizar departamento (Admin)
- `PATCH /api/departamentos/{id}/` - Actualizar departamento (Admin)
- `DELETE /api/departamentos/{id}/` - Eliminar departamento (Admin)

### Sensores
- `GET /api/sensores/` - Listar sensores (Autenticado)
- `GET /api/sensores/{id}/` - Detalle de sensor (Autenticado)
- `POST /api/sensores/` - Crear sensor (Admin)
- `PUT /api/sensores/{id}/` - Actualizar sensor (Admin)
- `PATCH /api/sensores/{id}/` - Actualizar sensor (Admin)
- `DELETE /api/sensores/{id}/` - Eliminar sensor (Admin)
- `POST /api/sensores/{id}/cambiar_estado/` - Cambiar estado del sensor (Admin)

**Ejemplo de crear sensor:**
```json
POST /api/sensores/
Headers: Authorization: Bearer {token}
{
  "codigo_uid": "RFID001",
  "nombre": "Sensor Recepción",
  "estado": "activo",
  "departamento": 1
}
```

### Barreras
- `GET /api/barreras/` - Listar barreras (Autenticado)
- `GET /api/barreras/{id}/` - Detalle de barrera (Autenticado)
- `POST /api/barreras/` - Crear barrera (Admin)
- `PUT /api/barreras/{id}/` - Actualizar barrera (Admin)
- `PATCH /api/barreras/{id}/` - Actualizar barrera (Admin)
- `DELETE /api/barreras/{id}/` - Eliminar barrera (Admin)
- `POST /api/barreras/{id}/abrir/` - Abrir barrera manualmente (Admin)
- `POST /api/barreras/{id}/cerrar/` - Cerrar barrera manualmente (Admin)

### Eventos
- `GET /api/eventos/` - Listar eventos (Autenticado)
- `GET /api/eventos/{id}/` - Detalle de evento (Autenticado)
- `POST /api/eventos/` - Crear evento manualmente (Admin)
- `POST /api/eventos/intentar_acceso/` - Simular intento de acceso desde sensor (Autenticado)

**Ejemplo de intento de acceso:**
```json
POST /api/eventos/intentar_acceso/
Headers: Authorization: Bearer {token}
{
  "codigo_uid": "RFID001",
  "barrera_id": 1
}

Respuesta (éxito):
{
  "acceso": true,
  "mensaje": "Acceso permitido",
  "sensor": "Sensor Recepción",
  "barrera": "Barrera Principal",
  "evento_id": 1
}

Respuesta (denegado):
{
  "acceso": false,
  "mensaje": "Acceso denegado - Sensor no registrado",
  "evento_id": 2
}
```

## 🔐 Autenticación JWT

Todas las rutas (excepto `/api/info/` y `/api/token/`) requieren autenticación JWT.

### Cómo usar el token:

1. **Obtener token:**
   ```
   POST /api/token/
   Body: {"username": "admin", "password": "admin123"}
   ```

2. **Usar token en requests:**
   ```
   Headers:
   Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
   ```

3. **Refrescar token (cuando expire):**
   ```
   POST /api/token/refresh/
   Body: {"refresh": "tu_refresh_token"}
   ```

## 📝 Permisos

- **Admin**: Acceso completo (CRUD en todas las entidades)
- **Operador**: Solo lectura (GET) en todas las entidades

## ⚠️ Códigos de Estado HTTP

- `200` - OK (operación exitosa)
- `201` - Created (recurso creado)
- `400` - Bad Request (error de validación)
- `401` - Unauthorized (no autenticado, falta token o token inválido)
- `403` - Forbidden (no tiene permisos para la acción)
- `404` - Not Found (recurso no encontrado o ruta inexistente)
- `500` - Internal Server Error (error del servidor)

## 🧪 Pruebas en Apidog/Postman

### 1. Probar endpoint de información
```
GET http://localhost:8000/api/info/
Sin headers necesarios
```

### 2. Obtener token JWT
```
POST http://localhost:8000/api/token/
Body (JSON):
{
  "username": "admin",
  "password": "admin123"
}
```

### 3. Listar departamentos (con token)
```
GET http://localhost:8000/api/departamentos/
Headers:
  Authorization: Bearer {tu_token_aqui}
```

### 4. Crear un sensor
```
POST http://localhost:8000/api/sensores/
Headers:
  Authorization: Bearer {tu_token_aqui}
Body (JSON):
{
  "codigo_uid": "RFID001",
  "nombre": "Sensor Recepción",
  "estado": "activo",
  "departamento": 1
}
```

### 5. Simular intento de acceso
```
POST http://localhost:8000/api/eventos/intentar_acceso/
Headers:
  Authorization: Bearer {tu_token_aqui}
Body (JSON):
{
  "codigo_uid": "RFID001",
  "barrera_id": 1
}
```

### 6. Probar sin token (debe dar 401)
```
GET http://localhost:8000/api/departamentos/
Sin headers
```

### 7. Probar con operador (debe permitir GET, pero no POST)
```
POST http://localhost:8000/api/departamentos/
Headers:
  Authorization: Bearer {token_operador}
Body: {...}
Debería retornar 403
```

## 🏗️ Arquitectura del Proyecto

```
SmartConnect-BackEnd/
├── core/                          # Aplicación principal
│   ├── models.py                 # Modelos: Usuario, Departamento, Sensor, Barrera, Evento
│   ├── serializers.py            # Serializadores para cada modelo
│   ├── views.py                  # ViewSets y vistas personalizadas
│   ├── permissions.py            # Permisos personalizados (IsAdminOrReadOnly, IsAdmin)
│   ├── exceptions.py             # Manejo personalizado de excepciones
│   ├── admin.py                  # Configuración del admin de Django
│   └── management/
│       └── commands/
│           └── create_initial_data.py  # Comando para crear datos iniciales
├── smartconnect/                 # Configuración del proyecto
│   ├── settings.py              # Configuración Django + DRF + JWT
│   ├── urls.py                  # URLs principales
│   ├── wsgi.py                  # WSGI config para producción
│   └── asgi.py                  # ASGI config
├── requirements.txt              # Dependencias del proyecto
└── db.sqlite3                   # Base de datos SQLite
```

## 📊 Modelos y Relaciones

### Usuario (Custom User Model)
- Hereda de AbstractUser
- Campo adicional: `rol` (admin/operador)
- Relación: Uno a muchos con Sensor, Evento

### Departamento
- Campos: nombre, descripcion
- Relaciones: Uno a muchos con Sensor, Barrera

### Sensor
- Campos: codigo_uid (único), nombre, estado, fecha_registro
- Relaciones: Muchos a uno con Departamento y Usuario, Uno a muchos con Evento
- Estados: activo, inactivo, bloqueado, perdido

### Barrera
- Campos: nombre, estado, ultima_apertura
- Relaciones: Muchos a uno con Departamento, Uno a muchos con Evento
- Estados: abierta, cerrada

### Evento
- Campos: tipo_acceso, origen, observaciones, fecha_evento
- Relaciones: Muchos a uno con Sensor, Barrera, Usuario
- Tipos: permitido, denegado
- Origen: automatico, manual

## 🔧 Configuración para AWS

### 1. Actualizar settings.py para producción:

```python
DEBUG = False
ALLOWED_HOSTS = ['tu-ip-aws.ec2.amazonaws.com', 'tu-dominio.com']
SECRET_KEY = os.environ.get('SECRET_KEY', 'tu-secret-key-super-segura')
```

### 2. Instalar gunicorn (ya incluido en requirements.txt)

### 3. Crear archivo `gunicorn_config.py`:

```python
bind = "0.0.0.0:8000"
workers = 3
timeout = 120
```

### 4. Ejecutar en AWS:

```bash
gunicorn smartconnect.wsgi:application --config gunicorn_config.py
```

### 5. Configurar Nginx (opcional, recomendado):

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📋 Validaciones Implementadas

- **MAC/UID**: No puede repetirse, mínimo 4 caracteres
- **Nombres**: Mínimo 3 caracteres
- **Estados**: Solo valores válidos según choices
- **Contraseñas**: Validación de Django (mínimo 8 caracteres, etc.)
- **Relaciones**: Validación de existencia de objetos relacionados

## 🐛 Manejo de Errores

Todos los errores retornan JSON con estructura consistente:

```json
{
  "error": true,
  "message": "Descripción del error",
  "details": {
    // Detalles específicos del error
  }
}
```

## 📝 Notas Importantes

1. **Base de datos**: Si cambias los modelos después de crear la BD, elimina `db.sqlite3` y vuelve a ejecutar migraciones.

2. **Secret Key**: En producción, usa una SECRET_KEY segura y no la expongas en el código.

3. **CORS**: En producción, configura `CORS_ALLOWED_ORIGINS` con los dominios permitidos, no uses `CORS_ALLOW_ALL_ORIGINS = True`.

4. **Usuarios iniciales**: Los usuarios `admin` y `operador` se crean automáticamente con el comando `create_initial_data`.

5. **Token JWT**: Los tokens expiran en 24 horas. Usa el endpoint de refresh para obtener nuevos tokens.

## 📞 Soporte

Para cualquier duda o problema, revisa:
- Los logs del servidor Django
- La consola del navegador (para errores CORS)
- Los mensajes de error retornados por la API en formato JSON

