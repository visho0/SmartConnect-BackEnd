# 📋 Descripción Técnica de Endpoints - SmartConnect API

## Endpoints Públicos (No requieren Token JWT)

---

### 1. GET `/` - Vista Raíz

**URL:** `/`

**Método:** `GET`

**Descripción:** Muestra información de bienvenida y lista todos los endpoints disponibles en la API.

**Código HTTP:** `200 OK`

**Token JWT:** ❌ No requerido

**JSON de Entrada:** No aplica (GET sin body)

**JSON de Salida:**
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
  },
  "documentacion": "Consulta el README.md para más información sobre los endpoints",
  "nota": "La mayoría de endpoints requieren autenticación JWT. Usa /api/token/ para obtener un token."
}
```

---

### 2. GET `/api/info/` - Información del Proyecto

**URL:** `/api/info/`

**Método:** `GET`

**Descripción:** Devuelve información sobre el proyecto, autor, asignatura y descripción del sistema.

**Código HTTP:** `200 OK`

**Token JWT:** ❌ No requerido

**JSON de Entrada:** No aplica (GET sin body)

**JSON de Salida:**
```json
{
  "autor": ["Pablo Carvajal, Vicente Durán"],
  "asignatura": "Programación Back End",
  "proyecto": "SmartConnect API",
  "descripcion": "API RESTful para sistema de control de acceso inteligente con sensores RFID, gestión de usuarios, departamentos, barreras y eventos de acceso. Diseñada para integración con aplicaciones móviles e IoT.",
  "version": "1.0"
}
```

---

## Endpoints de Autenticación

---

### 3. POST `/api/token/` - Login (Obtener Token)

**URL:** `/api/token/`

**Método:** `POST`

**Descripción:** Autentica un usuario con username y password, devuelve tokens JWT (access y refresh) para usar en endpoints protegidos.

**Código HTTP:** 
- `200 OK` (éxito)
- `401 Unauthorized` (credenciales inválidas)

**Token JWT:** ❌ No requerido

**JSON de Entrada:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**JSON de Salida (200 OK):**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NjM0ODM3MiwiaWF0IjoxNzY1NzQzNTcyLCJqdGkiOiI2ZTk3OGNmMzUxYWM0M2M2OTA0NTU3YmQ4NjZjZTUzOCIsInVzZXJfaWQiOjEsInJvbCI6ImFkbWluIiwidXNlcm5hbWUiOiJhZG1pbiJ9.EtZqDRoFcCqLPqUMJ7rTcYSFyMXZMwBfqAu8N-gJpjQ",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY1ODI5OTcyLCJpYXQiOjE3NjU3NDM1NzIsImp0aSI6IjdhMGEzYTlkODNkZTRmOWY5YzA1YTQ0MWVmNTYyY2MyIiwidXNlcl9pZCI6MSwicm9sIjoiYWRtaW4iLCJ1c2VybmFtZSI6ImFkbWluIn0.lpR1pScyVUcEp3yZCWeYyJ4d3P_hyBXvPAzQpek88TU"
}
```

**JSON de Salida (401 Unauthorized):**
```json
{
  "detail": "No active account found with the given credentials"
}
```

---

### 4. POST `/api/token/refresh/` - Renovar Token

**URL:** `/api/token/refresh/`

**Método:** `POST`

**Descripción:** Renueva el token de acceso (access) usando el refresh token cuando el access token ha expirado.

**Código HTTP:** 
- `200 OK` (éxito)
- `401 Unauthorized` (refresh token inválido o expirado)

**Token JWT:** ❌ No requerido (pero necesita refresh token en el body)

**JSON de Entrada:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**JSON de Salida (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## Endpoints de Usuarios (Requieren Token JWT - Solo Admin)

---

### 5. GET `/api/usuarios/` - Listar Usuarios

**URL:** `/api/usuarios/`

**Método:** `GET`

**Descripción:** Lista todos los usuarios registrados en el sistema. Solo accesible para administradores.

**Código HTTP:** 
- `200 OK` (éxito)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:** No aplica (GET sin body)

**JSON de Salida (200 OK):**
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "rol": "admin",
    "first_name": "",
    "last_name": ""
  },
  {
    "id": 2,
    "username": "operador",
    "email": "operador@example.com",
    "rol": "operador",
    "first_name": "Operador",
    "last_name": "Sistema"
  }
]
```

---

### 6. POST `/api/usuarios/` - Crear Usuario

**URL:** `/api/usuarios/`

**Método:** `POST`

**Descripción:** Crea un nuevo usuario en el sistema. Solo accesible para administradores.

**Código HTTP:** 
- `201 Created` (creado exitosamente)
- `400 Bad Request` (error de validación)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:**
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

**JSON de Salida (201 Created):**
```json
{
  "id": 3,
  "username": "nuevo_usuario",
  "email": "usuario@example.com",
  "rol": "operador",
  "first_name": "Nombre",
  "last_name": "Apellido",
  "fecha_creacion": "2024-01-15T10:30:00Z",
  "fecha_actualizacion": "2024-01-15T10:30:00Z"
}
```

**JSON de Salida (400 Bad Request):**
```json
{
  "error": true,
  "message": "Error de validación",
  "details": {
    "password": ["Las contraseñas no coinciden."],
    "username": ["Este campo es requerido."]
  }
}
```

---

### 7. GET `/api/usuarios/{id}/` - Detalle de Usuario

**URL:** `/api/usuarios/{id}/`

**Método:** `GET`

**Descripción:** Obtiene los detalles completos de un usuario específico por su ID.

**Código HTTP:** 
- `200 OK` (éxito)
- `404 Not Found` (usuario no encontrado)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:** No aplica (GET sin body)

**JSON de Salida (200 OK):**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "rol": "admin",
  "first_name": "",
  "last_name": "",
  "fecha_creacion": "2024-01-15T10:00:00Z",
  "fecha_actualizacion": "2024-01-15T10:00:00Z"
}
```

---

### 8. PUT `/api/usuarios/{id}/` - Actualizar Usuario

**URL:** `/api/usuarios/{id}/`

**Método:** `PUT`

**Descripción:** Actualiza completamente un usuario existente. Requiere enviar todos los campos.

**Código HTTP:** 
- `200 OK` (actualizado exitosamente)
- `400 Bad Request` (error de validación)
- `404 Not Found` (usuario no encontrado)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:**
```json
{
  "username": "admin_actualizado",
  "email": "admin_nuevo@example.com",
  "password": "nueva_password123",
  "password_confirm": "nueva_password123",
  "rol": "admin",
  "first_name": "Admin",
  "last_name": "Sistema"
}
```

**JSON de Salida (200 OK):**
```json
{
  "id": 1,
  "username": "admin_actualizado",
  "email": "admin_nuevo@example.com",
  "rol": "admin",
  "first_name": "Admin",
  "last_name": "Sistema",
  "fecha_creacion": "2024-01-15T10:00:00Z",
  "fecha_actualizacion": "2024-01-15T11:00:00Z"
}
```

---

### 9. PATCH `/api/usuarios/{id}/` - Actualizar Parcialmente Usuario

**URL:** `/api/usuarios/{id}/`

**Método:** `PATCH`

**Descripción:** Actualiza solo los campos específicos enviados de un usuario.

**Código HTTP:** 
- `200 OK` (actualizado exitosamente)
- `400 Bad Request` (error de validación)
- `404 Not Found` (usuario no encontrado)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:**
```json
{
  "email": "nuevo_email@example.com",
  "first_name": "Nuevo Nombre"
}
```

**JSON de Salida (200 OK):**
```json
{
  "id": 1,
  "username": "admin",
  "email": "nuevo_email@example.com",
  "rol": "admin",
  "first_name": "Nuevo Nombre",
  "last_name": "",
  "fecha_creacion": "2024-01-15T10:00:00Z",
  "fecha_actualizacion": "2024-01-15T11:30:00Z"
}
```

---

### 10. DELETE `/api/usuarios/{id}/` - Eliminar Usuario

**URL:** `/api/usuarios/{id}/`

**Método:** `DELETE`

**Descripción:** Elimina un usuario del sistema permanentemente.

**Código HTTP:** 
- `204 No Content` (eliminado exitosamente)
- `404 Not Found` (usuario no encontrado)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:** No aplica (DELETE sin body)

**JSON de Salida:** No hay contenido (204 No Content)

---

### 11. GET `/api/usuarios/me/` - Información del Usuario Actual

**URL:** `/api/usuarios/me/`

**Método:** `GET`

**Descripción:** Obtiene la información del usuario autenticado actualmente (el que tiene el token).

**Código HTTP:** 
- `200 OK` (éxito)
- `401 Unauthorized` (no autenticado)

**Token JWT:** ✅ Sí, requerido

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:** No aplica (GET sin body)

**JSON de Salida (200 OK):**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "rol": "admin",
  "first_name": "",
  "last_name": ""
}
```

---

## Endpoints de Departamentos (Requieren Token JWT)

---

### 12. GET `/api/departamentos/` - Listar Departamentos

**URL:** `/api/departamentos/`

**Método:** `GET`

**Descripción:** Lista todos los departamentos registrados en el sistema. Accesible para usuarios autenticados (admin y operador).

**Código HTTP:** 
- `200 OK` (éxito)
- `401 Unauthorized` (no autenticado)

**Token JWT:** ✅ Sí, requerido

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:** No aplica (GET sin body)

**JSON de Salida (200 OK):**
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
  },
  {
    "id": 2,
    "nombre": "Almacén",
    "descripcion": "Área de almacenamiento",
    "sensores_count": 0,
    "barreras_count": 0,
    "fecha_creacion": "2024-01-15T11:00:00Z",
    "fecha_actualizacion": "2024-01-15T11:00:00Z"
  }
]
```

---

### 13. POST `/api/departamentos/` - Crear Departamento

**URL:** `/api/departamentos/`

**Método:** `POST`

**Descripción:** Crea un nuevo departamento en el sistema. Solo accesible para administradores.

**Código HTTP:** 
- `201 Created` (creado exitosamente)
- `400 Bad Request` (error de validación)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (operador no puede crear)

**Token JWT:** ✅ Sí, requerido (rol: admin para crear)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:**
```json
{
  "nombre": "Almacén",
  "descripcion": "Área de almacenamiento de productos"
}
```

**JSON de Salida (201 Created):**
```json
{
  "id": 2,
  "nombre": "Almacén",
  "descripcion": "Área de almacenamiento de productos",
  "sensores_count": 0,
  "barreras_count": 0,
  "fecha_creacion": "2024-01-15T11:00:00Z",
  "fecha_actualizacion": "2024-01-15T11:00:00Z"
}
```

**JSON de Salida (400 Bad Request):**
```json
{
  "error": true,
  "message": "Error de validación",
  "details": {
    "nombre": ["Este campo es requerido."]
  }
}
```

**JSON de Salida (403 Forbidden - Operador):**
```json
{
  "error": true,
  "message": "No tiene permisos para realizar esta acción",
  "details": {
    "permission": "Acceso denegado"
  }
}
```

---

### 14. GET `/api/departamentos/{id}/` - Detalle de Departamento

**URL:** `/api/departamentos/{id}/`

**Método:** `GET`

**Descripción:** Obtiene los detalles completos de un departamento específico por su ID.

**Código HTTP:** 
- `200 OK` (éxito)
- `404 Not Found` (departamento no encontrado)
- `401 Unauthorized` (no autenticado)

**Token JWT:** ✅ Sí, requerido

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:** No aplica (GET sin body)

**JSON de Salida (200 OK):**
```json
{
  "id": 1,
  "nombre": "Recepción",
  "descripcion": "Área de recepción principal",
  "sensores_count": 2,
  "barreras_count": 1,
  "fecha_creacion": "2024-01-15T10:00:00Z",
  "fecha_actualizacion": "2024-01-15T10:00:00Z"
}
```

---

### 15. PUT `/api/departamentos/{id}/` - Actualizar Departamento

**URL:** `/api/departamentos/{id}/`

**Método:** `PUT`

**Descripción:** Actualiza completamente un departamento existente. Solo accesible para administradores.

**Código HTTP:** 
- `200 OK` (actualizado exitosamente)
- `400 Bad Request` (error de validación)
- `404 Not Found` (departamento no encontrado)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:**
```json
{
  "nombre": "Recepción Principal",
  "descripcion": "Área de recepción actualizada"
}
```

**JSON de Salida (200 OK):**
```json
{
  "id": 1,
  "nombre": "Recepción Principal",
  "descripcion": "Área de recepción actualizada",
  "sensores_count": 2,
  "barreras_count": 1,
  "fecha_creacion": "2024-01-15T10:00:00Z",
  "fecha_actualizacion": "2024-01-15T12:00:00Z"
}
```

---

### 16. PATCH `/api/departamentos/{id}/` - Actualizar Parcialmente Departamento

**URL:** `/api/departamentos/{id}/`

**Método:** `PATCH`

**Descripción:** Actualiza solo los campos específicos enviados de un departamento. Solo accesible para administradores.

**Código HTTP:** 
- `200 OK` (actualizado exitosamente)
- `400 Bad Request` (error de validación)
- `404 Not Found` (departamento no encontrado)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:**
```json
{
  "descripcion": "Nueva descripción del departamento"
}
```

**JSON de Salida (200 OK):**
```json
{
  "id": 1,
  "nombre": "Recepción",
  "descripcion": "Nueva descripción del departamento",
  "sensores_count": 2,
  "barreras_count": 1,
  "fecha_creacion": "2024-01-15T10:00:00Z",
  "fecha_actualizacion": "2024-01-15T12:30:00Z"
}
```

---

### 17. DELETE `/api/departamentos/{id}/` - Eliminar Departamento

**URL:** `/api/departamentos/{id}/`

**Método:** `DELETE`

**Descripción:** Elimina un departamento del sistema permanentemente. Solo accesible para administradores.

**Código HTTP:** 
- `204 No Content` (eliminado exitosamente)
- `404 Not Found` (departamento no encontrado)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:** No aplica (DELETE sin body)

**JSON de Salida:** No hay contenido (204 No Content)

---

## Endpoints de Sensores (Requieren Token JWT)

---

### 18. GET `/api/sensores/` - Listar Sensores

**URL:** `/api/sensores/`

**Método:** `GET`

**Descripción:** Lista todos los sensores RFID registrados en el sistema.

**Código HTTP:** 
- `200 OK` (éxito)
- `401 Unauthorized` (no autenticado)

**Token JWT:** ✅ Sí, requerido

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:** No aplica (GET sin body)

**JSON de Salida (200 OK):**
```json
[
  {
    "id": 1,
    "codigo_uid": "RFID001",
    "nombre": "Sensor Recepción",
    "estado": "activo",
    "departamento": 1,
    "departamento_nombre": "Recepción",
    "usuario": 1,
    "usuario_username": "admin",
    "fecha_registro": "2024-01-15T10:00:00Z",
    "fecha_actualizacion": "2024-01-15T10:00:00Z"
  }
]
```

---

### 19. POST `/api/sensores/` - Crear Sensor

**URL:** `/api/sensores/`

**Método:** `POST`

**Descripción:** Crea un nuevo sensor RFID en el sistema. Solo accesible para administradores.

**Código HTTP:** 
- `201 Created` (creado exitosamente)
- `400 Bad Request` (error de validación)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:**
```json
{
  "codigo_uid": "RFID002",
  "nombre": "Sensor Almacén",
  "estado": "activo",
  "departamento": 2,
  "usuario": 2
}
```

**JSON de Salida (201 Created):**
```json
{
  "id": 2,
  "codigo_uid": "RFID002",
  "nombre": "Sensor Almacén",
  "estado": "activo",
  "departamento": 2,
  "departamento_nombre": "Almacén",
  "usuario": 2,
  "usuario_username": "operador",
  "fecha_registro": "2024-01-15T11:00:00Z",
  "fecha_actualizacion": "2024-01-15T11:00:00Z"
}
```

---

### 20. GET `/api/sensores/{id}/` - Detalle de Sensor

**URL:** `/api/sensores/{id}/`

**Método:** `GET`

**Descripción:** Obtiene los detalles completos de un sensor específico por su ID.

**Código HTTP:** 
- `200 OK` (éxito)
- `404 Not Found` (sensor no encontrado)
- `401 Unauthorized` (no autenticado)

**Token JWT:** ✅ Sí, requerido

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:** No aplica (GET sin body)

**JSON de Salida (200 OK):**
```json
{
  "id": 1,
  "codigo_uid": "RFID001",
  "nombre": "Sensor Recepción",
  "estado": "activo",
  "departamento": 1,
  "departamento_nombre": "Recepción",
  "usuario": 1,
  "usuario_username": "admin",
  "fecha_registro": "2024-01-15T10:00:00Z",
  "fecha_actualizacion": "2024-01-15T10:00:00Z"
}
```

---

### 21. PUT `/api/sensores/{id}/` - Actualizar Sensor

**URL:** `/api/sensores/{id}/`

**Método:** `PUT`

**Descripción:** Actualiza completamente un sensor existente. Solo accesible para administradores.

**Código HTTP:** 
- `200 OK` (actualizado exitosamente)
- `400 Bad Request` (error de validación)
- `404 Not Found` (sensor no encontrado)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:**
```json
{
  "codigo_uid": "RFID001",
  "nombre": "Sensor Recepción Actualizado",
  "estado": "activo",
  "departamento": 1,
  "usuario": 1
}
```

**JSON de Salida (200 OK):**
```json
{
  "id": 1,
  "codigo_uid": "RFID001",
  "nombre": "Sensor Recepción Actualizado",
  "estado": "activo",
  "departamento": 1,
  "departamento_nombre": "Recepción",
  "usuario": 1,
  "usuario_username": "admin",
  "fecha_registro": "2024-01-15T10:00:00Z",
  "fecha_actualizacion": "2024-01-15T13:00:00Z"
}
```

---

### 22. PATCH `/api/sensores/{id}/` - Actualizar Parcialmente Sensor

**URL:** `/api/sensores/{id}/`

**Método:** `PATCH`

**Descripción:** Actualiza solo los campos específicos enviados de un sensor. Solo accesible para administradores.

**Código HTTP:** 
- `200 OK` (actualizado exitosamente)
- `400 Bad Request` (error de validación)
- `404 Not Found` (sensor no encontrado)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:**
```json
{
  "estado": "inactivo"
}
```

**JSON de Salida (200 OK):**
```json
{
  "id": 1,
  "codigo_uid": "RFID001",
  "nombre": "Sensor Recepción",
  "estado": "inactivo",
  "departamento": 1,
  "departamento_nombre": "Recepción",
  "usuario": 1,
  "usuario_username": "admin",
  "fecha_registro": "2024-01-15T10:00:00Z",
  "fecha_actualizacion": "2024-01-15T13:30:00Z"
}
```

---

### 23. DELETE `/api/sensores/{id}/` - Eliminar Sensor

**URL:** `/api/sensores/{id}/`

**Método:** `DELETE`

**Descripción:** Elimina un sensor del sistema permanentemente. Solo accesible para administradores.

**Código HTTP:** 
- `204 No Content` (eliminado exitosamente)
- `404 Not Found` (sensor no encontrado)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:** No aplica (DELETE sin body)

**JSON de Salida:** No hay contenido (204 No Content)

---

### 24. POST `/api/sensores/{id}/cambiar_estado/` - Cambiar Estado del Sensor

**URL:** `/api/sensores/{id}/cambiar_estado/`

**Método:** `POST`

**Descripción:** Cambia el estado de un sensor (activo, inactivo, bloqueado, perdido). Solo accesible para administradores.

**Código HTTP:** 
- `200 OK` (actualizado exitosamente)
- `400 Bad Request` (estado inválido)
- `404 Not Found` (sensor no encontrado)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:**
```json
{
  "estado": "bloqueado"
}
```

**JSON de Salida (200 OK):**
```json
{
  "id": 1,
  "codigo_uid": "RFID001",
  "nombre": "Sensor Recepción",
  "estado": "bloqueado",
  "departamento": 1,
  "departamento_nombre": "Recepción",
  "usuario": 1,
  "usuario_username": "admin",
  "fecha_registro": "2024-01-15T10:00:00Z",
  "fecha_actualizacion": "2024-01-15T14:00:00Z"
}
```

**JSON de Salida (400 Bad Request):**
```json
{
  "error": true,
  "message": "Estado inválido",
  "details": {
    "estado": "Debe ser uno de: activo, inactivo, bloqueado, perdido"
  }
}
```

---

## Endpoints de Barreras (Requieren Token JWT)

---

### 25. GET `/api/barreras/` - Listar Barreras

**URL:** `/api/barreras/`

**Método:** `GET`

**Descripción:** Lista todas las barreras registradas en el sistema.

**Código HTTP:** 
- `200 OK` (éxito)
- `401 Unauthorized` (no autenticado)

**Token JWT:** ✅ Sí, requerido

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:** No aplica (GET sin body)

**JSON de Salida (200 OK):**
```json
[
  {
    "id": 1,
    "nombre": "Barrera Principal",
    "estado": "cerrada",
    "departamento": 1,
    "departamento_nombre": "Recepción",
    "fecha_creacion": "2024-01-15T10:00:00Z",
    "fecha_actualizacion": "2024-01-15T10:00:00Z",
    "ultima_apertura": null
  }
]
```

---

### 26. POST `/api/barreras/` - Crear Barrera

**URL:** `/api/barreras/`

**Método:** `POST`

**Descripción:** Crea una nueva barrera en el sistema. Solo accesible para administradores.

**Código HTTP:** 
- `201 Created` (creado exitosamente)
- `400 Bad Request` (error de validación)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:**
```json
{
  "nombre": "Barrera Secundaria",
  "estado": "cerrada",
  "departamento": 2
}
```

**JSON de Salida (201 Created):**
```json
{
  "id": 2,
  "nombre": "Barrera Secundaria",
  "estado": "cerrada",
  "departamento": 2,
  "departamento_nombre": "Almacén",
  "fecha_creacion": "2024-01-15T11:00:00Z",
  "fecha_actualizacion": "2024-01-15T11:00:00Z",
  "ultima_apertura": null
}
```

---

### 27. GET `/api/barreras/{id}/` - Detalle de Barrera

**URL:** `/api/barreras/{id}/`

**Método:** `GET`

**Descripción:** Obtiene los detalles completos de una barrera específica por su ID.

**Código HTTP:** 
- `200 OK` (éxito)
- `404 Not Found` (barrera no encontrada)
- `401 Unauthorized` (no autenticado)

**Token JWT:** ✅ Sí, requerido

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:** No aplica (GET sin body)

**JSON de Salida (200 OK):**
```json
{
  "id": 1,
  "nombre": "Barrera Principal",
  "estado": "cerrada",
  "departamento": 1,
  "departamento_nombre": "Recepción",
  "fecha_creacion": "2024-01-15T10:00:00Z",
  "fecha_actualizacion": "2024-01-15T10:00:00Z",
  "ultima_apertura": null
}
```

---

### 28. PUT `/api/barreras/{id}/` - Actualizar Barrera

**URL:** `/api/barreras/{id}/`

**Método:** `PUT`

**Descripción:** Actualiza completamente una barrera existente. Solo accesible para administradores.

**Código HTTP:** 
- `200 OK` (actualizado exitosamente)
- `400 Bad Request` (error de validación)
- `404 Not Found` (barrera no encontrada)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:**
```json
{
  "nombre": "Barrera Principal Actualizada",
  "estado": "cerrada",
  "departamento": 1
}
```

**JSON de Salida (200 OK):**
```json
{
  "id": 1,
  "nombre": "Barrera Principal Actualizada",
  "estado": "cerrada",
  "departamento": 1,
  "departamento_nombre": "Recepción",
  "fecha_creacion": "2024-01-15T10:00:00Z",
  "fecha_actualizacion": "2024-01-15T15:00:00Z",
  "ultima_apertura": null
}
```

---

### 29. PATCH `/api/barreras/{id}/` - Actualizar Parcialmente Barrera

**URL:** `/api/barreras/{id}/`

**Método:** `PATCH`

**Descripción:** Actualiza solo los campos específicos enviados de una barrera. Solo accesible para administradores.

**Código HTTP:** 
- `200 OK` (actualizado exitosamente)
- `400 Bad Request` (error de validación)
- `404 Not Found` (barrera no encontrada)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:**
```json
{
  "estado": "abierta"
}
```

**JSON de Salida (200 OK):**
```json
{
  "id": 1,
  "nombre": "Barrera Principal",
  "estado": "abierta",
  "departamento": 1,
  "departamento_nombre": "Recepción",
  "fecha_creacion": "2024-01-15T10:00:00Z",
  "fecha_actualizacion": "2024-01-15T15:30:00Z",
  "ultima_apertura": null
}
```

---

### 30. DELETE `/api/barreras/{id}/` - Eliminar Barrera

**URL:** `/api/barreras/{id}/`

**Método:** `DELETE`

**Descripción:** Elimina una barrera del sistema permanentemente. Solo accesible para administradores.

**Código HTTP:** 
- `204 No Content` (eliminado exitosamente)
- `404 Not Found` (barrera no encontrada)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:** No aplica (DELETE sin body)

**JSON de Salida:** No hay contenido (204 No Content)

---

### 31. POST `/api/barreras/{id}/abrir/` - Abrir Barrera

**URL:** `/api/barreras/{id}/abrir/`

**Método:** `POST`

**Descripción:** Abre una barrera manualmente y registra un evento de acceso permitido con origen manual.

**Código HTTP:** 
- `200 OK` (abierta exitosamente)
- `404 Not Found` (barrera no encontrada)
- `401 Unauthorized` (no autenticado)

**Token JWT:** ✅ Sí, requerido

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:** No aplica (POST sin body)

**JSON de Salida (200 OK):**
```json
{
  "id": 1,
  "nombre": "Barrera Principal",
  "estado": "abierta",
  "departamento": 1,
  "departamento_nombre": "Recepción",
  "fecha_creacion": "2024-01-15T10:00:00Z",
  "fecha_actualizacion": "2024-01-15T16:00:00Z",
  "ultima_apertura": "2024-01-15T16:00:00Z"
}
```

---

### 32. POST `/api/barreras/{id}/cerrar/` - Cerrar Barrera

**URL:** `/api/barreras/{id}/cerrar/`

**Método:** `POST`

**Descripción:** Cierra una barrera manualmente.

**Código HTTP:** 
- `200 OK` (cerrada exitosamente)
- `404 Not Found` (barrera no encontrada)
- `401 Unauthorized` (no autenticado)

**Token JWT:** ✅ Sí, requerido

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:** No aplica (POST sin body)

**JSON de Salida (200 OK):**
```json
{
  "id": 1,
  "nombre": "Barrera Principal",
  "estado": "cerrada",
  "departamento": 1,
  "departamento_nombre": "Recepción",
  "fecha_creacion": "2024-01-15T10:00:00Z",
  "fecha_actualizacion": "2024-01-15T16:30:00Z",
  "ultima_apertura": "2024-01-15T16:00:00Z"
}
```

---

## Endpoints de Eventos (Requieren Token JWT)

---

### 33. GET `/api/eventos/` - Listar Eventos

**URL:** `/api/eventos/`

**Método:** `GET`

**Descripción:** Lista todos los eventos de acceso registrados en el sistema, ordenados por fecha más reciente.

**Código HTTP:** 
- `200 OK` (éxito)
- `401 Unauthorized` (no autenticado)

**Token JWT:** ✅ Sí, requerido

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:** No aplica (GET sin body)

**JSON de Salida (200 OK):**
```json
[
  {
    "id": 1,
    "sensor": 1,
    "sensor_nombre": "Sensor Recepción",
    "sensor_codigo": "RFID001",
    "barrera": 1,
    "barrera_nombre": "Barrera Principal",
    "tipo_acceso": "permitido",
    "origen": "automatico",
    "usuario_operador": null,
    "usuario_operador_username": null,
    "observaciones": "Acceso permitido automáticamente",
    "fecha_evento": "2024-01-15T10:30:00Z"
  }
]
```

---

### 34. POST `/api/eventos/` - Crear Evento

**URL:** `/api/eventos/`

**Método:** `POST`

**Descripción:** Crea un nuevo evento de acceso manualmente. Solo accesible para administradores.

**Código HTTP:** 
- `201 Created` (creado exitosamente)
- `400 Bad Request` (error de validación)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:**
```json
{
  "sensor": 1,
  "barrera": 1,
  "tipo_acceso": "permitido",
  "origen": "manual",
  "observaciones": "Apertura manual desde API"
}
```

**JSON de Salida (201 Created):**
```json
{
  "id": 2,
  "sensor": 1,
  "sensor_nombre": "Sensor Recepción",
  "sensor_codigo": "RFID001",
  "barrera": 1,
  "barrera_nombre": "Barrera Principal",
  "tipo_acceso": "permitido",
  "origen": "manual",
  "usuario_operador": 1,
  "usuario_operador_username": "admin",
  "observaciones": "Apertura manual desde API",
  "fecha_evento": "2024-01-15T17:00:00Z"
}
```

---

### 35. GET `/api/eventos/{id}/` - Detalle de Evento

**URL:** `/api/eventos/{id}/`

**Método:** `GET`

**Descripción:** Obtiene los detalles completos de un evento específico por su ID.

**Código HTTP:** 
- `200 OK` (éxito)
- `404 Not Found` (evento no encontrado)
- `401 Unauthorized` (no autenticado)

**Token JWT:** ✅ Sí, requerido

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:** No aplica (GET sin body)

**JSON de Salida (200 OK):**
```json
{
  "id": 1,
  "sensor": 1,
  "sensor_nombre": "Sensor Recepción",
  "sensor_codigo": "RFID001",
  "barrera": 1,
  "barrera_nombre": "Barrera Principal",
  "tipo_acceso": "permitido",
  "origen": "automatico",
  "usuario_operador": null,
  "usuario_operador_username": null,
  "observaciones": "Acceso permitido automáticamente",
  "fecha_evento": "2024-01-15T10:30:00Z"
}
```

---

### 36. PUT `/api/eventos/{id}/` - Actualizar Evento

**URL:** `/api/eventos/{id}/`

**Método:** `PUT`

**Descripción:** Actualiza completamente un evento existente. Solo accesible para administradores.

**Código HTTP:** 
- `200 OK` (actualizado exitosamente)
- `400 Bad Request` (error de validación)
- `404 Not Found` (evento no encontrado)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:**
```json
{
  "sensor": 1,
  "barrera": 1,
  "tipo_acceso": "denegado",
  "origen": "manual",
  "observaciones": "Acceso denegado manualmente"
}
```

**JSON de Salida (200 OK):**
```json
{
  "id": 1,
  "sensor": 1,
  "sensor_nombre": "Sensor Recepción",
  "sensor_codigo": "RFID001",
  "barrera": 1,
  "barrera_nombre": "Barrera Principal",
  "tipo_acceso": "denegado",
  "origen": "manual",
  "usuario_operador": 1,
  "usuario_operador_username": "admin",
  "observaciones": "Acceso denegado manualmente",
  "fecha_evento": "2024-01-15T10:30:00Z"
}
```

---

### 37. PATCH `/api/eventos/{id}/` - Actualizar Parcialmente Evento

**URL:** `/api/eventos/{id}/`

**Método:** `PATCH`

**Descripción:** Actualiza solo los campos específicos enviados de un evento. Solo accesible para administradores.

**Código HTTP:** 
- `200 OK` (actualizado exitosamente)
- `400 Bad Request` (error de validación)
- `404 Not Found` (evento no encontrado)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:**
```json
{
  "observaciones": "Observaciones actualizadas"
}
```

**JSON de Salida (200 OK):**
```json
{
  "id": 1,
  "sensor": 1,
  "sensor_nombre": "Sensor Recepción",
  "sensor_codigo": "RFID001",
  "barrera": 1,
  "barrera_nombre": "Barrera Principal",
  "tipo_acceso": "permitido",
  "origen": "automatico",
  "usuario_operador": null,
  "usuario_operador_username": null,
  "observaciones": "Observaciones actualizadas",
  "fecha_evento": "2024-01-15T10:30:00Z"
}
```

---

### 38. DELETE `/api/eventos/{id}/` - Eliminar Evento

**URL:** `/api/eventos/{id}/`

**Método:** `DELETE`

**Descripción:** Elimina un evento del sistema permanentemente. Solo accesible para administradores.

**Código HTTP:** 
- `204 No Content` (eliminado exitosamente)
- `404 Not Found` (evento no encontrado)
- `401 Unauthorized` (no autenticado)
- `403 Forbidden` (no es admin)

**Token JWT:** ✅ Sí, requerido (rol: admin)

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:** No aplica (DELETE sin body)

**JSON de Salida:** No hay contenido (204 No Content)

---

### 39. POST `/api/eventos/intentar_acceso/` - Simular Intento de Acceso

**URL:** `/api/eventos/intentar_acceso/`

**Método:** `POST`

**Descripción:** Simula un intento de acceso desde un sensor RFID. Valida el sensor, su estado, y si el acceso es permitido, abre la barrera automáticamente y registra el evento.

**Código HTTP:** 
- `200 OK` (acceso permitido)
- `400 Bad Request` (error de validación)
- `403 Forbidden` (acceso denegado)
- `404 Not Found` (barrera no encontrada)
- `401 Unauthorized` (no autenticado)

**Token JWT:** ✅ Sí, requerido

**Headers:** `Authorization: Bearer {token}`

**JSON de Entrada:**
```json
{
  "codigo_uid": "RFID001",
  "barrera_id": 1
}
```

**JSON de Salida (200 OK - Acceso Permitido):**
```json
{
  "acceso": true,
  "mensaje": "Acceso permitido",
  "sensor": "Sensor Recepción",
  "barrera": "Barrera Principal",
  "evento_id": 5
}
```

**JSON de Salida (403 Forbidden - Sensor No Registrado):**
```json
{
  "acceso": false,
  "mensaje": "Acceso denegado - Sensor no registrado",
  "evento_id": 6
}
```

**JSON de Salida (403 Forbidden - Sensor Inactivo):**
```json
{
  "acceso": false,
  "mensaje": "Acceso denegado - Sensor Inactivo",
  "evento_id": 7
}
```

**JSON de Salida (404 Not Found - Barrera No Encontrada):**
```json
{
  "error": true,
  "message": "Barrera no encontrada",
  "details": {
    "barrera_id": "ID inválido"
  }
}
```

**JSON de Salida (400 Bad Request - Validación):**
```json
{
  "error": true,
  "message": "Error de validación",
  "details": {
    "codigo_uid": ["Este campo es requerido."],
    "barrera_id": ["Este campo es requerido."]
  }
}
```

---

## Resumen de Endpoints

| Categoría | Cantidad | Endpoints |
|-----------|----------|-----------|
| **Públicos** | 2 | `/`, `/api/info/` |
| **Autenticación** | 2 | `/api/token/`, `/api/token/refresh/` |
| **Usuarios** | 7 | CRUD completo + `/me/` |
| **Departamentos** | 6 | CRUD completo |
| **Sensores** | 7 | CRUD + `/cambiar_estado/` |
| **Barreras** | 8 | CRUD + `/abrir/`, `/cerrar/` |
| **Eventos** | 7 | CRUD + `/intentar_acceso/` |
| **TOTAL** | **39** | Endpoints |

---

**Nota:** Todos los endpoints que requieren token JWT deben incluir el header `Authorization: Bearer {token}` donde `{token}` es el valor del campo `access` obtenido del endpoint `/api/token/`.

