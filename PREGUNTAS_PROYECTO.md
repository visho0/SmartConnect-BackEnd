# 📋 Preguntas y Respuestas sobre la Arquitectura del Proyecto SmartConnect

## 🏗️ ESTRUCTURA GENERAL

### ¿Qué framework y tecnologías utiliza este proyecto?
**Respuesta:** Django 6.0 + Django REST Framework. Autenticación con JWT (JSON Web Tokens) usando `djangorestframework-simplejwt`. Base de datos: PostgreSQL en producción (AWS RDS) o SQLite en desarrollo.

### ¿Cómo está organizada la estructura de carpetas?
**Respuesta:** 
- `core/`: Aplicación principal con modelos, vistas, serializadores, permisos y excepciones
- `smartconnect/`: Configuración del proyecto (settings, urls, wsgi)
- `manage.py`: Script de gestión Django

### ¿Cuántas entidades tiene el proyecto?
**Respuesta:** 5 entidades: Usuario, Departamento, Sensor, Barrera y Evento.

---

## 🔐 SEGURIDAD Y AUTENTICACIÓN

### ¿Cómo se maneja la seguridad de las contraseñas?
**Respuesta:** 
- Las contraseñas se validan con los validadores nativos de Django (`validate_password`)
- Se almacenan usando `set_password()` que las hashea con PBKDF2
- Se requiere confirmación de contraseña (`password_confirm`) al crear usuarios
- Validadores activos: longitud mínima, similitud con datos del usuario, contraseñas comunes y numéricas

### ¿Cómo funciona la autenticación JWT?
**Respuesta:**
- Se usa `rest_framework_simplejwt` para generar tokens
- Token de acceso válido por 24 horas
- Token de refresh válido por 7 días
- Los tokens incluyen información adicional: `rol` y `username`
- Se envían en el header: `Authorization: Bearer <token>`

### ¿Dónde se configura la autenticación JWT?
**Respuesta:** En `smartconnect/settings.py` en la sección `SIMPLE_JWT` y `REST_FRAMEWORK`.

---

## ✅ VALIDACIONES

### ¿Cómo se validan los datos de entrada?
**Respuesta:** 
- **En los modelos:** Validadores de campo (ej: `MinLengthValidator`) y método `clean()`
- **En los serializadores:** Métodos `validate()` y `validate_<campo>()`
- **Validaciones específicas:**
  - Contraseñas deben coincidir
  - Código UID debe ser único
  - Nombres deben tener mínimo 3 caracteres

### ¿Dónde se validan las contraseñas?
**Respuesta:** En `core/serializers.py` en `UsuarioSerializer`:
- Se valida que coincidan `password` y `password_confirm`
- Se usa `validate_password` de Django para validar fortaleza

### ¿Cómo se valida la unicidad del código UID de los sensores?
**Respuesta:** En `SensorSerializer.validate_codigo_uid()` se verifica que no exista otro sensor con el mismo código UID (exceptuando el actual en caso de actualización).

---

## 🔑 PERMISOS Y AUTORIZACIÓN

### ¿Qué sistema de permisos utiliza?
**Respuesta:** Permisos personalizados en `core/permissions.py`:
- `IsAdminOrReadOnly`: Admin puede hacer CRUD completo, Operador solo lectura (GET)
- `IsAdmin`: Solo administradores pueden acceder

### ¿Cómo se aplican los permisos?
**Respuesta:** Se asignan a nivel de ViewSet en `core/views.py`:
- `UsuarioViewSet`: Solo admin (`IsAdmin`)
- `DepartamentoViewSet`, `SensorViewSet`, `BarreraViewSet`, `EventoViewSet`: Admin o lectura (`IsAdminOrReadOnly`)

### ¿Qué roles de usuario existen?
**Respuesta:** Dos roles: `admin` (Administrador) y `operador` (Operador). Definidos en el modelo `Usuario`.

---

## 🗄️ BASE DE DATOS

### ¿Qué base de datos se usa?
**Respuesta:** 
- **Desarrollo:** SQLite (`db.sqlite3`)
- **Producción:** PostgreSQL (AWS RDS)
- La configuración se detecta automáticamente según variables de entorno

### ¿Cómo se configuran las bases de datos?
**Respuesta:** En `smartconnect/settings.py`:
- Si existen variables `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` → PostgreSQL
- Si no existen → SQLite

---

## 📡 ENDPOINTS Y RUTAS

### ¿Cómo se definen las rutas?
**Respuesta:** En `smartconnect/urls.py`:
- Se usa `DefaultRouter` de DRF para ViewSets
- Endpoints principales: `/api/usuarios/`, `/api/departamentos/`, `/api/sensores/`, `/api/barreras/`, `/api/eventos/`
- Autenticación: `/api/token/` (login) y `/api/token/refresh/` (refresh)

### ¿Qué endpoints públicos existen?
**Respuesta:** 
- `GET /`: Vista de bienvenida
- `GET /api/info/`: Información del proyecto
- `POST /api/token/`: Login (obtener token)

### ¿Qué acciones personalizadas tienen los ViewSets?
**Respuesta:**
- `UsuarioViewSet`: `me/` (obtener usuario autenticado)
- `SensorViewSet`: `cambiar_estado/` (cambiar estado del sensor)
- `BarreraViewSet`: `abrir/` y `cerrar/` (control manual)
- `EventoViewSet`: `intentar_acceso/` (simular acceso desde sensor RFID)

---

## 📦 SERIALIZADORES

### ¿Qué serializadores existen?
**Respuesta:**
- `UsuarioSerializer`: Crear/actualizar usuarios (con validación de contraseñas)
- `UsuarioListSerializer`: Listar usuarios (sin contraseñas)
- `DepartamentoSerializer`: Incluye contadores de sensores y barreras
- `SensorSerializer`: Incluye nombres de departamento y usuario relacionados
- `BarreraSerializer`: Incluye nombre del departamento
- `EventoSerializer`: Incluye información relacionada (sensor, barrera, usuario)
- `AccesoSerializer`: Validar intentos de acceso desde sensores

### ¿Cómo se manejan los campos relacionados?
**Respuesta:** Se usan `SerializerMethodField` y `source` para incluir información relacionada sin exponer IDs directamente (ej: `departamento_nombre`, `usuario_username`).

---

## ⚠️ MANEJO DE ERRORES

### ¿Cómo se manejan las excepciones?
**Respuesta:** En `core/exceptions.py` hay un `custom_exception_handler` que:
- Formatea todas las respuestas de error en JSON consistente
- Estructura: `{error: true, message: "...", details: {...}}`
- Maneja códigos: 400 (validación), 401 (no autenticado), 403 (sin permisos), 404 (no encontrado)

### ¿Dónde se registra el handler de excepciones?
**Respuesta:** En `smartconnect/settings.py` en `REST_FRAMEWORK['EXCEPTION_HANDLER']`.

---

## ⚙️ CONFIGURACIÓN

### ¿Cómo se manejan las variables de entorno?
**Respuesta:** Se usa `python-decouple` (con fallback si no está instalado):
- Lee variables de `.env` o variables de entorno del sistema
- Valores por defecto si no existen
- Variables importantes: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, credenciales de BD

### ¿Qué middleware está activo?
**Respuesta:** 
- `SecurityMiddleware`: Seguridad básica
- `CorsMiddleware`: Manejo de CORS
- `CsrfViewMiddleware`: Protección CSRF
- `AuthenticationMiddleware`: Autenticación de usuarios
- Y otros middlewares estándar de Django

### ¿Cómo se configura CORS?
**Respuesta:** En `smartconnect/settings.py`:
- `CORS_ALLOW_ALL_ORIGINS = True` (solo desarrollo)
- `CORS_ALLOWED_ORIGINS` lista específica de orígenes permitidos

---

## 🔄 RELACIONES ENTRE MODELOS

### ¿Cómo se relacionan las entidades?
**Respuesta:**
- **Usuario** → **Sensor** (1:N, ForeignKey)
- **Usuario** → **Evento** (1:N, ForeignKey como `usuario_operador`)
- **Departamento** → **Sensor** (1:N, ForeignKey)
- **Departamento** → **Barrera** (1:N, ForeignKey)
- **Sensor** → **Evento** (1:N, ForeignKey)
- **Barrera** → **Evento** (1:N, ForeignKey)

### ¿Qué estrategias de eliminación se usan?
**Respuesta:**
- `CASCADE`: Eliminar eventos si se elimina sensor/barrera
- `SET_NULL`: Poner `null` en relaciones opcionales (ej: sensor sin departamento)

---

## 🚀 DESPLIEGUE

### ¿Cómo se despliega en producción?
**Respuesta:**
- Servidor: AWS EC2 con Gunicorn
- Base de datos: AWS RDS (PostgreSQL)
- Servidor web: Nginx como proxy reverso
- Configuración: Variables de entorno para producción

### ¿Qué archivos de configuración hay para despliegue?
**Respuesta:**
- `gunicorn_config.py`: Configuración de Gunicorn
- `deploy_scripts/`: Scripts de despliegue
- Documentación: `DEPLOY_AWS.md`, `GUIA_CONEXION_EC2.md`

---

## 📊 PAGINACIÓN Y RENDERING

### ¿Cómo se maneja la paginación?
**Respuesta:** Configurada en `REST_FRAMEWORK`:
- Clase: `PageNumberPagination`
- Tamaño de página: 20 elementos

### ¿Qué formato de respuesta se usa?
**Respuesta:** Solo JSON (`JSONRenderer`). No hay HTML ni otros formatos.

---

## 🔍 OPTIMIZACIONES

### ¿Qué optimizaciones de consultas hay?
**Respuesta:** 
- `select_related()` en ViewSets para evitar consultas N+1:
  - `SensorViewSet`: `select_related('departamento', 'usuario')`
  - `BarreraViewSet`: `select_related('departamento')`
  - `EventoViewSet`: `select_related('sensor', 'barrera', 'usuario_operador')`
- Índices en campos frecuentemente consultados (ej: `codigo_uid`, `fecha_evento`)

---

## 📝 NOTAS ADICIONALES

### ¿Qué funcionalidad especial tiene el sistema de acceso?
**Respuesta:** 
- Endpoint `intentar_acceso/` simula acceso desde sensor RFID
- Valida que el sensor exista y esté activo
- Crea eventos automáticamente (permitido/denegado)
- Actualiza estado de barrera al permitir acceso

### ¿Cómo se personaliza el token JWT?
**Respuesta:** En `CustomTokenObtainPairSerializer` se agregan campos personalizados (`rol` y `username`) al payload del token.

