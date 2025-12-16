# 🔌 Guía Rápida: Conectarse a EC2 desde Windows

## 📍 Dónde encontrar la información necesaria

### 1. IP Pública de tu EC2

1. Ve a **AWS Console** → **EC2** → **Instances**
2. Selecciona tu instancia `smartconnect-api-server`
3. En la parte inferior, busca **Public IPv4 address**
4. Copia esa IP (ejemplo: `54.123.45.67`)

### 2. Archivo .pem (Key Pair)

**Si ya lo tienes:**
- Busca el archivo `.pem` que descargaste al crear el Key Pair
- Ejemplo: `smartconnect-key.pem`

**Si no lo tienes:**
1. Ve a **EC2 Console** → **Key Pairs** → **Create key pair**
2. Nombre: `smartconnect-key`
3. Tipo: RSA
4. Formato: `.pem`
5. Click **Create key pair** (se descarga automáticamente)
6. **GUARDA este archivo en un lugar seguro** (lo necesitarás cada vez)

## 🚀 Opción 1: EC2 Instance Connect (MÁS FÁCIL - Recomendado)

### Ventajas:
- ✅ No necesitas el archivo .pem
- ✅ Funciona directamente desde el navegador
- ✅ No requiere configuración en tu máquina
- ✅ Perfecto para principiantes

### Pasos:

1. **Abre AWS Console** → **EC2** → **Instances**

2. **Selecciona tu instancia** `smartconnect-api-server`

3. Click en el botón **"Connect"** (arriba)

4. Selecciona la pestaña **"EC2 Instance Connect"**

5. Click en **"Connect"**

6. **¡Listo!** Se abrirá una terminal en tu navegador donde puedes ejecutar comandos

7. Ya puedes ejecutar los comandos del Paso 4:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   sudo apt install -y python3-pip python3-venv postgresql-client nginx supervisor
   ```

## 💻 Opción 2: SSH desde PowerShell (Windows)

### Requisitos:
- Windows 10/11 con OpenSSH instalado (viene por defecto)

### Pasos:

1. **Abre PowerShell** (click derecho → "Ejecutar como administrador")

2. **Navega a la carpeta donde está tu archivo .pem:**
   ```powershell
   cd C:\Users\PulentoPepe\Downloads
   # o donde tengas tu archivo .pem
   ```

3. **Cambia los permisos del archivo .pem** (solo primera vez):
   ```powershell
   icacls.exe smartconnect-key.pem /inheritance:r
   icacls.exe smartconnect-key.pem /grant:r "$($env:USERNAME):(R)"
   ```

4. **Conéctate a EC2:**
   ```powershell
   ssh -i smartconnect-key.pem ubuntu@TU-IP-PUBLICA
   ```
   Reemplaza `TU-IP-PUBLICA` con la IP que copiaste

5. Si te pregunta si quieres continuar, escribe `yes` y presiona Enter

6. **¡Estás conectado!** Ya puedes ejecutar los comandos del Paso 4

## 🐚 Opción 3: SSH desde Git Bash (Si tienes Git instalado)

### Pasos:

1. **Abre Git Bash**

2. **Navega a la carpeta con tu .pem:**
   ```bash
   cd /c/Users/PulentoPepe/Downloads
   ```

3. **Cambia permisos:**
   ```bash
   chmod 400 smartconnect-key.pem
   ```

4. **Conéctate:**
   ```bash
   ssh -i smartconnect-key.pem ubuntu@TU-IP-PUBLICA
   ```

5. **¡Estás conectado!**

## 🔧 Opción 4: WSL (Windows Subsystem for Linux)

Si tienes WSL instalado, puedes usar SSH normalmente:

```bash
chmod 400 smartconnect-key.pem
ssh -i smartconnect-key.pem ubuntu@TU-IP-PUBLICA
```

## ⚠️ Problemas Comunes

### Error: "Permission denied (publickey)"

**Solución:**
- Verifica que el archivo .pem tenga los permisos correctos
- Asegúrate de usar el usuario correcto: `ubuntu` (no `ec2-user` que es para Amazon Linux)
- Verifica que estás usando la IP pública correcta

### Error: "Connection timed out"

**Solución:**
- Verifica que el Security Group de tu EC2 permita SSH (puerto 22) desde tu IP
- Ve a **EC2** → **Security Groups** → Tu security group
- Edita **Inbound rules** y asegúrate de que haya una regla para SSH (22) desde tu IP o desde cualquier lugar (0.0.0.0/0)

### Error: "The authenticity of host can't be established"

**Solución:**
- Es normal la primera vez
- Escribe `yes` y presiona Enter

## ✅ Verificación Rápida

Una vez conectado, prueba estos comandos para verificar:

```bash
# Verificar que eres ubuntu
whoami
# Debe mostrar: ubuntu

# Verificar sistema
lsb_release -a
# Debe mostrar Ubuntu 22.04

# Verificar conectividad
ping -c 3 google.com
```

## 📝 Resumen - Qué necesitas antes del Paso 4:

1. ✅ Instancia EC2 creada y corriendo
2. ✅ IP pública de la instancia EC2
3. ✅ Key Pair (.pem) descargado (solo si usas SSH, no necesario para Instance Connect)
4. ✅ Security Group configurado para permitir SSH (puerto 22)

## 🎯 Recomendación

**Para empezar rápido:** Usa **EC2 Instance Connect** (Opción 1)
- Es la forma más fácil
- No requiere configuración
- Funciona desde el navegador

**Para uso profesional:** Aprende a usar **SSH** (Opción 2 o 3)
- Más rápido para comandos repetitivos
- Mejor para scripts automatizados
- Habilidades transferibles

¡Una vez conectado, puedes continuar con el Paso 4 de la guía! 🚀



