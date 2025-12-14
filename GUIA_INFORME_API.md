# 📋 Guía Completa para el Informe de API - SmartConnect

Esta guía te ayudará a responder todas las preguntas del informe usando Apidog.

---

## 1. ARQUITECTURA GENERAL

### Descripción de la Estructura del Proyecto

**SmartConnect** es una API RESTful desarrollada con **Django 6.0** y **Django REST Framework** para un sistema de control de acceso inteligente con sensores RFID.

### Componentes Principales:

1. **Backend Framework**: Django 6.0 + Django REST Framework
2. **Base de Datos**: PostgreSQL (producción en AWS RDS) / SQLite (desarrollo)
3. **Autenticación**: JWT (JSON Web Tokens) usando `djangorestframework-simplejwt`
4. **Servidor Web**: Gunicorn + Nginx
5. **Despliegue**: AWS EC2 (servidor) + AWS RDS (base de datos)

### Estructura de Carpetas:

```
SmartConnect-BackEnd/
├── core/                    # Aplicación principal
│   ├── models.py           # Modelos de datos
│   ├── views.py            # Vistas y ViewSets
│   ├── serializers.py     # Serializadores
│   ├── permissions.py      # Permisos personalizados
│   └── exceptions.py       # Manejo de errores
├── smartconnect/           # Configuración del proyecto
│   ├── settings.py        # Configuración Django
│   └── urls.py            # Rutas de la API
└── manage.py              # Script de gestión Django
```

---

## 2. MODELOS Y SUS RELACIONES (Modelo Lógico)

### Diagrama de Relaciones:

```
Usuario (AbstractUser)
├── id (PK)
├── username
├── email
├── rol (admin/operador)
└── fecha_creacion

Departamento
├── id (PK)
├── nombre (unique)
├── descripcion
└── fecha_creacion
    │
    ├── Sensor (1:N)
    │   ├── id (PK)
    │   ├── codigo_uid (unique)
    │   ├── nombre
    │   ├── estado (activo/inactivo/bloqueado/perdido)
    │   ├── departamento_id (FK → Departamento)
    │   └── usuario_id (FK → Usuario, nullable)
    │
    └── Barrera (1:N)
        ├── id (PK)
        ├── nombre
        ├── estado (abierta/cerrada)
        ├── departamento_id (FK → Departamento, nullable)
        └── ultima_apertura

Evento
├── id (PK)
├── sensor_id (FK → Sensor, nullable)
├── barrera_id (FK → Barrera)
├── tipo_acceso (permitido/denegado)
├── origen (automatico/manual)
├── usuario_operador_id (FK → Usuario, nullable)
├── observaciones
└── fecha_evento
```

### Descripción de Modelos:

1. **Usuario**: Usuario personalizado con roles (admin/operador)
2. **Departamento**: Zonas o áreas del sistema
3. **Sensor**: Sensores RFID con código UID único
4. **Barrera**: Barreras de acceso físicas
5. **Evento**: Registro de intentos de acceso (permitidos/denegados)

---

## 3. ENDPOINTS CREADOS

### Endpoints Públicos (No requieren token):

#### 1. GET `/` - Vista raíz
- **Método**: GET
- **Descripción**: Muestra información de bienvenida y lista de endpoints disponibles
- **Código HTTP**: 200
- **Token JWT**: No requerido
- **Ejemplo de respuesta**:
```json
{
  "mensaje": "Bienvenido a SmartConnect API",
  "version": "1.0",
  "endpoints": {
    "informacion": "/api/info/",
    "autenticacion": {
      "login": "/api/token/",
      "refresh": "/api/token/refresh/"
    },
    "recursos": {
      "usuarios": "/api/usuarios/",
      "departamentos": "/api/departamentos/",
      "sensores": "/api/sensores/",
      "barreras": "/api/barreras/",
      "eventos": "/api/eventos/"
    }
  }
}
```

#### 2. GET `/api/info/` - Información del proyecto
- **Método**: GET
- **Descripción**: Información sobre el proyecto, autor y asignatura
- **Código HTTP**: 200
- **Token JWT**: No requerido
- **Ejemplo de respuesta**:
```json
{
  "autor": ["Tu Nombre"],
  "asignatura": "Programación Back End",
  "proyecto": "SmartConnect API",
  "descripcion": "API RESTful para sistema de control de acceso inteligente...",
  "version": "1.0"
}
```

### Endpoints de Autenticación:

#### 3. POST `/api/token/` - Login (Obtener token)
- **Método**: POST
- **Descripción**: Autentica un usuario y devuelve tokens JWT (access y refresh)
- **Código HTTP**: 200 (éxito), 401 (credenciales inválidas)
- **Token JWT**: No requerido
- **JSON de entrada**:
```json
{
  "username": "admin",
  "password": "admin123"
}
```
- **JSON de salida**:
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 4. POST `/api/token/refresh/` - Renovar token
- **Método**: POST
- **Descripción**: Renueva el token de acceso usando el refresh token
- **Código HTTP**: 200 (éxito), 401 (token inválido)
- **Token JWT**: No requerido (pero necesita refresh token en el body)
- **JSON de entrada**:
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Endpoints de Usuarios (Requieren token, solo Admin):

#### 5. GET `/api/usuarios/` - Listar usuarios
- **Método**: GET
- **Descripción**: Lista todos los usuarios (solo admin)
- **Código HTTP**: 200, 401 (no autenticado), 403 (no es admin)
- **Token JWT**: Sí, requerido (rol: admin)
- **Headers**: `Authorization: Bearer {token}`
- **JSON de salida**:
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "rol": "admin",
    "first_name": "",
    "last_name": ""
  }
]
```

#### 6. POST `/api/usuarios/` - Crear usuario
- **Método**: POST
- **Descripción**: Crea un nuevo usuario (solo admin)
- **Código HTTP**: 201 (creado), 400 (validación), 401, 403
- **Token JWT**: Sí, requerido (rol: admin)
- **JSON de entrada**:
```json
{
  "username": "nuevo_usuario",
  "email": "usuario@example.com",
  "password": "password123",
  "password_confirm": "password123",
  "rol": "operador",
  "first_name": "Nombre",
  "last_name": "Apellido"
}
```

#### 7. GET `/api/usuarios/{id}/` - Detalle de usuario
- **Método**: GET
- **Descripción**: Obtiene detalles de un usuario específico
- **Código HTTP**: 200, 404 (no encontrado), 401, 403
- **Token JWT**: Sí, requerido (rol: admin)

#### 8. PUT `/api/usuarios/{id}/` - Actualizar usuario
- **Método**: PUT
- **Descripción**: Actualiza un usuario completo
- **Código HTTP**: 200, 400, 404, 401, 403
- **Token JWT**: Sí, requerido (rol: admin)

#### 9. PATCH `/api/usuarios/{id}/` - Actualizar parcialmente
- **Método**: PATCH
- **Descripción**: Actualiza campos específicos de un usuario
- **Código HTTP**: 200, 400, 404, 401, 403
- **Token JWT**: Sí, requerido (rol: admin)

#### 10. DELETE `/api/usuarios/{id}/` - Eliminar usuario
- **Método**: DELETE
- **Descripción**: Elimina un usuario
- **Código HTTP**: 204 (sin contenido), 404, 401, 403
- **Token JWT**: Sí, requerido (rol: admin)

#### 11. GET `/api/usuarios/me/` - Información del usuario actual
- **Método**: GET
- **Descripción**: Obtiene información del usuario autenticado
- **Código HTTP**: 200, 401
- **Token JWT**: Sí, requerido

### Endpoints de Departamentos (Requieren token):

#### 12. GET `/api/departamentos/` - Listar departamentos
- **Método**: GET
- **Descripción**: Lista todos los departamentos
- **Código HTTP**: 200, 401
- **Token JWT**: Sí, requerido
- **JSON de salida**:
```json
[
  {
    "id": 1,
    "nombre": "Recepción",
    "descripcion": "Área de recepción principal",
    "sensores_count": 2,
    "barreras_count": 1,
    "fecha_creacion": "2024-01-15T10:00:00Z",
    "fecha_actualizacion": "2024-01-15T10:00:00Z"
  }
]
```

#### 13. POST `/api/departamentos/` - Crear departamento
- **Método**: POST
- **Descripción**: Crea un nuevo departamento (solo admin)
- **Código HTTP**: 201, 400, 401, 403 (operador no puede crear)
- **Token JWT**: Sí, requerido
- **JSON de entrada**:
```json
{
  "nombre": "Almacén",
  "descripcion": "Área de almacenamiento"
}
```

#### 14. GET `/api/departamentos/{id}/` - Detalle de departamento
- **Método**: GET
- **Descripción**: Obtiene detalles de un departamento
- **Código HTTP**: 200, 404, 401
- **Token JWT**: Sí, requerido

#### 15. PUT `/api/departamentos/{id}/` - Actualizar departamento
- **Método**: PUT
- **Descripción**: Actualiza un departamento (solo admin)
- **Código HTTP**: 200, 400, 404, 401, 403
- **Token JWT**: Sí, requerido

#### 16. DELETE `/api/departamentos/{id}/` - Eliminar departamento
- **Método**: DELETE
- **Descripción**: Elimina un departamento (solo admin)
- **Código HTTP**: 204, 404, 401, 403
- **Token JWT**: Sí, requerido

### Endpoints de Sensores (Requieren token):

#### 17. GET `/api/sensores/` - Listar sensores
- **Método**: GET
- **Descripción**: Lista todos los sensores
- **Código HTTP**: 200, 401
- **Token JWT**: Sí, requerido

#### 18. POST `/api/sensores/` - Crear sensor
- **Método**: POST
- **Descripción**: Crea un nuevo sensor (solo admin)
- **Código HTTP**: 201, 400, 401, 403
- **Token JWT**: Sí, requerido
- **JSON de entrada**:
```json
{
  "codigo_uid": "RFID001",
  "nombre": "Sensor Recepción",
  "estado": "activo",
  "departamento": 1,
  "usuario": 1
}
```

#### 19. GET `/api/sensores/{id}/` - Detalle de sensor
- **Método**: GET
- **Descripción**: Obtiene detalles de un sensor
- **Código HTTP**: 200, 404, 401
- **Token JWT**: Sí, requerido

#### 20. PUT `/api/sensores/{id}/` - Actualizar sensor
- **Método**: PUT
- **Descripción**: Actualiza un sensor (solo admin)
- **Código HTTP**: 200, 400, 404, 401, 403
- **Token JWT**: Sí, requerido

#### 21. DELETE `/api/sensores/{id}/` - Eliminar sensor
- **Método**: DELETE
- **Descripción**: Elimina un sensor (solo admin)
- **Código HTTP**: 204, 404, 401, 403
- **Token JWT**: Sí, requerido

#### 22. POST `/api/sensores/{id}/cambiar_estado/` - Cambiar estado del sensor
- **Método**: POST
- **Descripción**: Cambia el estado de un sensor (solo admin)
- **Código HTTP**: 200, 400, 404, 401, 403
- **Token JWT**: Sí, requerido
- **JSON de entrada**:
```json
{
  "estado": "bloqueado"
}
```

### Endpoints de Barreras (Requieren token):

#### 23. GET `/api/barreras/` - Listar barreras
- **Método**: GET
- **Descripción**: Lista todas las barreras
- **Código HTTP**: 200, 401
- **Token JWT**: Sí, requerido

#### 24. POST `/api/barreras/` - Crear barrera
- **Método**: POST
- **Descripción**: Crea una nueva barrera (solo admin)
- **Código HTTP**: 201, 400, 401, 403
- **Token JWT**: Sí, requerido
- **JSON de entrada**:
```json
{
  "nombre": "Barrera Principal",
  "estado": "cerrada",
  "departamento": 1
}
```

#### 25. GET `/api/barreras/{id}/` - Detalle de barrera
- **Método**: GET
- **Descripción**: Obtiene detalles de una barrera
- **Código HTTP**: 200, 404, 401
- **Token JWT**: Sí, requerido

#### 26. POST `/api/barreras/{id}/abrir/` - Abrir barrera
- **Método**: POST
- **Descripción**: Abre una barrera manualmente y registra evento
- **Código HTTP**: 200, 404, 401
- **Token JWT**: Sí, requerido

#### 27. POST `/api/barreras/{id}/cerrar/` - Cerrar barrera
- **Método**: POST
- **Descripción**: Cierra una barrera manualmente
- **Código HTTP**: 200, 404, 401
- **Token JWT**: Sí, requerido

### Endpoints de Eventos (Requieren token):

#### 28. GET `/api/eventos/` - Listar eventos
- **Método**: GET
- **Descripción**: Lista todos los eventos de acceso
- **Código HTTP**: 200, 401
- **Token JWT**: Sí, requerido

#### 29. POST `/api/eventos/intentar_acceso/` - Simular intento de acceso
- **Método**: POST
- **Descripción**: Simula un intento de acceso desde un sensor RFID
- **Código HTTP**: 200 (permitido), 403 (denegado), 400, 404
- **Token JWT**: Sí, requerido
- **JSON de entrada**:
```json
{
  "codigo_uid": "RFID001",
  "barrera_id": 1
}
```
- **JSON de salida (permitido)**:
```json
{
  "acceso": true,
  "mensaje": "Acceso permitido",
  "sensor": "Sensor Recepción",
  "barrera": "Barrera Principal",
  "evento_id": 5
}
```
- **JSON de salida (denegado)**:
```json
{
  "acceso": false,
  "mensaje": "Acceso denegado - Sensor no registrado",
  "evento_id": 6
}
```

---

## 4. PRUEBAS EN AWS

### URL Pública:
```
http://54.225.212.23
```

### Evidencias de Funcionamiento:

**1. Probar endpoint público:**
```bash
curl http://54.225.212.23/api/info/
```

**2. Probar login:**
```bash
curl -X POST http://54.225.212.23/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

**3. Probar endpoint protegido (con token):**
```bash
TOKEN="tu-token-aqui"
curl http://54.225.212.23/api/departamentos/ \
  -H "Authorization: Bearer $TOKEN"
```

### Capturas en Apidog:
- Captura de la respuesta de `/api/info/`
- Captura del login exitoso con token
- Captura de listar departamentos con token
- Captura de crear departamento
- Captura de actualizar departamento
- Captura de eliminar departamento

---

## 5. AUTENTICACIÓN JWT

### Cómo Funciona:

1. **Generación del Token:**
   - El usuario envía credenciales a `/api/token/`
   - El servidor valida las credenciales
   - Si son válidas, genera dos tokens:
     - **Access Token**: Válido por 24 horas
     - **Refresh Token**: Válido por 7 días
   - El token incluye: `user_id`, `rol`, `username`

2. **Envío del Token:**
   - Se envía en el header `Authorization`
   - Formato: `Authorization: Bearer {token_access}`
   - Ejemplo: `Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

3. **Rutas que Requieren Token:**
   - ✅ `/api/usuarios/` (todos los métodos)
   - ✅ `/api/departamentos/` (todos los métodos)
   - ✅ `/api/sensores/` (todos los métodos)
   - ✅ `/api/barreras/` (todos los métodos)
   - ✅ `/api/eventos/` (todos los métodos)
   - ❌ `/` (raíz - no requiere)
   - ❌ `/api/info/` (no requiere)
   - ❌ `/api/token/` (no requiere)
   - ❌ `/api/token/refresh/` (no requiere)

### Configuración JWT:
- **Algoritmo**: HS256
- **Access Token Lifetime**: 24 horas
- **Refresh Token Lifetime**: 7 días
- **Header Type**: Bearer

---

## 6. MANEJO DE ERRORES

### Validaciones Implementadas:

1. **Validación de Campos Requeridos**: Campos obligatorios no pueden estar vacíos
2. **Validación de Unicidad**: `codigo_uid` de sensores debe ser único
3. **Validación de Contraseñas**: Deben coincidir en creación de usuarios
4. **Validación de Estados**: Estados deben ser valores válidos (activo, inactivo, etc.)
5. **Validación de Relaciones**: Foreign keys deben existir

### Mensajes de Error:

#### 400 - Bad Request (Validación):
```json
{
  "error": true,
  "message": "Error de validación",
  "details": {
    "nombre": ["Este campo es requerido."],
    "codigo_uid": ["Este código UID/MAC ya está registrado."]
  }
}
```

#### 401 - Unauthorized (No autenticado):
```json
{
  "error": true,
  "message": "No autenticado. Se requiere token JWT válido",
  "details": {
    "authentication": "Token requerido o inválido"
  }
}
```

#### 403 - Forbidden (Sin permisos):
```json
{
  "error": true,
  "message": "No tiene permisos para realizar esta acción",
  "details": {
    "permission": "Acceso denegado"
  }
}
```

#### 404 - Not Found:
```json
{
  "error": true,
  "message": "Recurso no encontrado",
  "details": {
    "not_found": "No encontrado"
  }
}
```

#### 500 - Internal Server Error:
```json
{
  "error": true,
  "message": "Error interno del servidor",
  "details": {}
}
```

---

## 7. CAPTURAS DE PRUEBAS EN APIDOG

### Pruebas a Realizar:

#### 1. Login (Obtener Token)
- **URL**: `POST http://54.225.212.23/api/token/`
- **Body**: `{"username":"admin","password":"admin123"}`
- **Captura**: Respuesta con tokens access y refresh

#### 2. Listar Departamentos (Con Token)
- **URL**: `GET http://54.225.212.23/api/departamentos/`
- **Header**: `Authorization: Bearer {token}`
- **Captura**: Lista de departamentos

#### 3. Crear Departamento (Con Token)
- **URL**: `POST http://54.225.212.23/api/departamentos/`
- **Header**: `Authorization: Bearer {token}`
- **Body**: `{"nombre":"Nuevo Departamento","descripcion":"Descripción"}`
- **Captura**: Departamento creado (201)

#### 4. Actualizar Departamento (Con Token)
- **URL**: `PUT http://54.225.212.23/api/departamentos/{id}/`
- **Header**: `Authorization: Bearer {token}`
- **Body**: `{"nombre":"Departamento Actualizado","descripcion":"Nueva descripción"}`
- **Captura**: Departamento actualizado (200)

#### 5. Eliminar Departamento (Con Token)
- **URL**: `DELETE http://54.225.212.23/api/departamentos/{id}/`
- **Header**: `Authorization: Bearer {token}`
- **Captura**: Respuesta 204 (sin contenido)

#### 6. Prueba Sin Token
- **URL**: `GET http://54.225.212.23/api/departamentos/`
- **Sin header Authorization**
- **Captura**: Error 401

#### 7. Prueba Con Token Inválido
- **URL**: `GET http://54.225.212.23/api/departamentos/`
- **Header**: `Authorization: Bearer token_invalido`
- **Captura**: Error 401

#### 8. Prueba Con Operador (Sin Permisos para Crear)
- **URL**: `POST http://54.225.212.23/api/departamentos/`
- **Header**: `Authorization: Bearer {token_operador}`
- **Body**: `{"nombre":"Test"}`
- **Captura**: Error 403

---

## 📝 NOTAS PARA EL INFORME

1. **URL Base**: Siempre usa `http://54.225.212.23` en las capturas
2. **Token**: Copia el token completo desde la respuesta del login
3. **Headers**: Siempre incluye `Content-Type: application/json` en POST/PUT
4. **Códigos HTTP**: Anota el código de respuesta en cada captura
5. **Errores**: Incluye capturas de errores 400, 401, 403, 404

---

## 🎯 CHECKLIST DE CAPTURAS

- [ ] Login exitoso con token
- [ ] Listar departamentos (GET)
- [ ] Crear departamento (POST)
- [ ] Actualizar departamento (PUT)
- [ ] Eliminar departamento (DELETE)
- [ ] Error 401 sin token
- [ ] Error 401 con token inválido
- [ ] Error 403 con operador intentando crear
- [ ] Error 404 recurso no encontrado
- [ ] Error 400 validación incorrecta

---

¡Listo! Con esta guía puedes completar tu informe completo. 🚀

