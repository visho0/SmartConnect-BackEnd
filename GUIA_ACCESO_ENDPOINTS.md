# 📖 Guía Simple de Acceso a Endpoints - SmartConnect API

## 🔑 Paso 1: Obtener Token (Login)

**Todos los usuarios (admin y operador) deben hacer esto primero:**

### POST `/api/token/` - Login

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Respuesta:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**⚠️ IMPORTANTE:** Copia el valor de `access` para usar en los siguientes endpoints.

---

## 👤 Como ADMINISTRADOR

### Headers para TODOS los endpoints (excepto login):
```
Authorization: Bearer {tu-token-access}
Content-Type: application/json
```

---

### 📋 USUARIOS (Solo Admin)

#### GET `/api/usuarios/` - Listar usuarios
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### POST `/api/usuarios/` - Crear usuario
**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
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

---

#### GET `/api/usuarios/{id}/` - Ver usuario
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### PUT `/api/usuarios/{id}/` - Actualizar usuario completo
**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "username": "usuario_actualizado",
  "email": "nuevo@example.com",
  "password": "nueva_password",
  "password_confirm": "nueva_password",
  "rol": "admin",
  "first_name": "Nuevo",
  "last_name": "Nombre"
}
```

---

#### PATCH `/api/usuarios/{id}/` - Actualizar parcialmente
**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "email": "nuevo_email@example.com"
}
```

---

#### DELETE `/api/usuarios/{id}/` - Eliminar usuario
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### GET `/api/usuarios/me/` - Mi información
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

### 🏢 DEPARTAMENTOS

#### GET `/api/departamentos/` - Listar departamentos
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### POST `/api/departamentos/` - Crear departamento
**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "nombre": "Almacén",
  "descripcion": "Área de almacenamiento"
}
```

---

#### GET `/api/departamentos/{id}/` - Ver departamento
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### PUT `/api/departamentos/{id}/` - Actualizar completo
**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "nombre": "Almacén Principal",
  "descripcion": "Nueva descripción"
}
```

---

#### PATCH `/api/departamentos/{id}/` - Actualizar parcialmente
**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "descripcion": "Descripción actualizada"
}
```

---

#### DELETE `/api/departamentos/{id}/` - Eliminar departamento
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

### 📡 SENSORES

#### GET `/api/sensores/` - Listar sensores
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### POST `/api/sensores/` - Crear sensor
**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "codigo_uid": "RFID002",
  "nombre": "Sensor Almacén",
  "estado": "activo",
  "departamento": 1,
  "usuario": 2
}
```

---

#### GET `/api/sensores/{id}/` - Ver sensor
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### PUT `/api/sensores/{id}/` - Actualizar completo
**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "codigo_uid": "RFID002",
  "nombre": "Sensor Actualizado",
  "estado": "activo",
  "departamento": 1,
  "usuario": 1
}
```

---

#### PATCH `/api/sensores/{id}/` - Actualizar parcialmente
**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "estado": "inactivo"
}
```

---

#### DELETE `/api/sensores/{id}/` - Eliminar sensor
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### POST `/api/sensores/{id}/cambiar_estado/` - Cambiar estado
**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "estado": "bloqueado"
}
```

**Estados válidos:** `activo`, `inactivo`, `bloqueado`, `perdido`

---

### 🚧 BARRERAS

#### GET `/api/barreras/` - Listar barreras
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### POST `/api/barreras/` - Crear barrera
**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "nombre": "Barrera Secundaria",
  "estado": "cerrada",
  "departamento": 1
}
```

---

#### GET `/api/barreras/{id}/` - Ver barrera
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### PUT `/api/barreras/{id}/` - Actualizar completo
**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "nombre": "Barrera Actualizada",
  "estado": "cerrada",
  "departamento": 1
}
```

---

#### PATCH `/api/barreras/{id}/` - Actualizar parcialmente
**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "estado": "abierta"
}
```

---

#### DELETE `/api/barreras/{id}/` - Eliminar barrera
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### POST `/api/barreras/{id}/abrir/` - Abrir barrera
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### POST `/api/barreras/{id}/cerrar/` - Cerrar barrera
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

### 📝 EVENTOS

#### GET `/api/eventos/` - Listar eventos
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### POST `/api/eventos/` - Crear evento
**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "sensor": 1,
  "barrera": 1,
  "tipo_acceso": "permitido",
  "origen": "manual",
  "observaciones": "Apertura manual"
}
```

---

#### GET `/api/eventos/{id}/` - Ver evento
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### PUT `/api/eventos/{id}/` - Actualizar completo
**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "sensor": 1,
  "barrera": 1,
  "tipo_acceso": "denegado",
  "origen": "manual",
  "observaciones": "Actualizado"
}
```

---

#### PATCH `/api/eventos/{id}/` - Actualizar parcialmente
**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "observaciones": "Nuevas observaciones"
}
```

---

#### DELETE `/api/eventos/{id}/` - Eliminar evento
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### POST `/api/eventos/intentar_acceso/` - Simular acceso
**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "codigo_uid": "RFID001",
  "barrera_id": 1
}
```

---

## 👷 Como OPERADOR

### Headers para TODOS los endpoints (excepto login):
```
Authorization: Bearer {tu-token-access}
Content-Type: application/json
```

**⚠️ IMPORTANTE:** El operador SOLO puede hacer GET (leer). NO puede crear, actualizar ni eliminar.

---

### ✅ Lo que SÍ puede hacer (GET - Solo lectura):

#### GET `/api/departamentos/` - Listar departamentos
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### GET `/api/departamentos/{id}/` - Ver departamento
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### GET `/api/sensores/` - Listar sensores
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### GET `/api/sensores/{id}/` - Ver sensor
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### GET `/api/barreras/` - Listar barreras
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### GET `/api/barreras/{id}/` - Ver barrera
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### POST `/api/barreras/{id}/abrir/` - Abrir barrera
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### POST `/api/barreras/{id}/cerrar/` - Cerrar barrera
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### GET `/api/eventos/` - Listar eventos
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### GET `/api/eventos/{id}/` - Ver evento
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

#### POST `/api/eventos/intentar_acceso/` - Simular acceso
**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "codigo_uid": "RFID001",
  "barrera_id": 1
}
```

---

#### GET `/api/usuarios/me/` - Mi información
**Headers:**
```
Authorization: Bearer {token}
```

**Body:** No requiere

---

### ❌ Lo que NO puede hacer (403 Forbidden):

- ❌ POST `/api/departamentos/` - Crear departamento
- ❌ PUT/PATCH `/api/departamentos/{id}/` - Actualizar departamento
- ❌ DELETE `/api/departamentos/{id}/` - Eliminar departamento
- ❌ POST `/api/sensores/` - Crear sensor
- ❌ PUT/PATCH `/api/sensores/{id}/` - Actualizar sensor
- ❌ DELETE `/api/sensores/{id}/` - Eliminar sensor
- ❌ POST `/api/barreras/` - Crear barrera
- ❌ PUT/PATCH `/api/barreras/{id}/` - Actualizar barrera
- ❌ DELETE `/api/barreras/{id}/` - Eliminar barrera
- ❌ POST `/api/eventos/` - Crear evento
- ❌ PUT/PATCH `/api/eventos/{id}/` - Actualizar evento
- ❌ DELETE `/api/eventos/{id}/` - Eliminar evento
- ❌ Cualquier endpoint de `/api/usuarios/` (excepto `/me/`)

---

## 🌐 Endpoints Públicos (No requieren token)

### GET `/` - Vista raíz
**Headers:** No requiere

**Body:** No requiere

---

### GET `/api/info/` - Información del proyecto
**Headers:** No requiere

**Body:** No requiere

---

## 📝 Resumen Rápido

### Para ADMIN:
- ✅ Headers: `Authorization: Bearer {token}` + `Content-Type: application/json` (en POST/PUT/PATCH)
- ✅ Puede hacer: GET, POST, PUT, PATCH, DELETE en todos los recursos
- ✅ Puede gestionar usuarios

### Para OPERADOR:
- ✅ Headers: `Authorization: Bearer {token}`
- ✅ Puede hacer: Solo GET (leer datos)
- ✅ Puede: Abrir/cerrar barreras, simular acceso
- ❌ NO puede: Crear, actualizar, eliminar recursos

### Públicos:
- ✅ No requieren token
- ✅ Solo GET `/` y GET `/api/info/`

---

## 🔄 Renovar Token (cuando expire)

### POST `/api/token/refresh/` - Renovar access token

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Respuesta:**
```json
{
  "access": "nuevo-token-access-aqui"
}
```

---

## 💡 Tips

1. **Siempre copia el token `access` completo** (es muy largo)
2. **No olvides el espacio después de "Bearer"**
3. **El token expira en 24 horas** - usa `/api/token/refresh/` para renovarlo
4. **Operador solo puede leer** - si intenta crear/actualizar/eliminar recibirá 403
5. **URL base:** `http://54.225.212.23` (o tu IP pública de AWS)

