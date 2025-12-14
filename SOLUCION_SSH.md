# 🔧 Solución: Problemas de Conexión SSH a EC2

## ❌ Problema que estás viendo

Estás viendo un prompt de login de consola serial en lugar de una sesión SSH normal. Esto significa que el SSH no se está estableciendo correctamente.

## ✅ Solución Paso a Paso

### Paso 1: Verifica que tienes la IP pública correcta

1. Ve a **AWS Console** → **EC2** → **Instances**
2. Selecciona tu instancia
3. Busca **"Public IPv4 address"** (NO la IPv4 privada)
4. Debe verse algo como: `54.123.45.67` (NO como `172.31.x.x`)

⚠️ **IMPORTANTE:** Si ves una IP que empieza con `172.31.` o `10.0.`, esa es la IP **privada**, no la pública. Necesitas la **IP pública**.

### Paso 2: Ubica tu archivo .pem

Asegúrate de tener el archivo `claves_connect.pem` en una ubicación accesible, por ejemplo:
- `C:\Users\PulentoPepe\Downloads\claves_connect.pem`
- O donde lo hayas guardado

### Paso 3: Conéctate correctamente desde PowerShell

1. **Abre PowerShell** (NO el símbolo del sistema)

2. **Navega a la carpeta donde está tu .pem:**
   ```powershell
   cd C:\Users\PulentoPepe\Downloads
   # Ajusta la ruta según donde tengas tu archivo
   ```

3. **Cambia permisos del archivo (solo primera vez):**
   ```powershell
   icacls.exe claves_connect.pem /inheritance:r
   icacls.exe claves_connect.pem /grant:r "$($env:USERNAME):(R)"
   ```

4. **Conéctate usando la IP pública real:**
   ```powershell
   ssh -i claves_connect.pem ubuntu@TU-IP-PUBLICA-REAL
   ```
   
   Reemplaza `TU-IP-PUBLICA-REAL` con la IP pública que copiaste (debe ser diferente de 172.31.x.x)

### Ejemplo completo:

```powershell
# 1. Navegar a la carpeta
cd C:\Users\PulentoPepe\Downloads

# 2. Verificar que el archivo existe
dir claves_connect.pem

# 3. Cambiar permisos (solo primera vez)
icacls.exe claves_connect.pem /inheritance:r
icacls.exe claves_connect.pem /grant:r "$($env:USERNAME):(R)"

# 4. Conectarse (reemplaza 54.123.45.67 con tu IP pública real)
ssh -i claves_connect.pem ubuntu@54.123.45.67
```

## 🔍 Si sigues teniendo problemas

### Verificar que el Security Group permite SSH

1. Ve a **EC2** → **Security Groups**
2. Selecciona el security group de tu instancia
3. **Inbound rules** debe tener:
   - Type: SSH
   - Port: 22
   - Source: 0.0.0.0/0 (o tu IP específica)

### Verificar que la instancia está corriendo

1. Ve a **EC2** → **Instances**
2. Tu instancia debe estar en estado **"running"** (verde)
3. Debe tener una **IP pública asignada**

### Alternativa: Usa EC2 Instance Connect (MÁS FÁCIL)

Si SSH te sigue dando problemas, usa EC2 Instance Connect:

1. **AWS Console** → **EC2** → **Instances**
2. Selecciona tu instancia
3. Click **"Connect"**
4. Pestaña **"EC2 Instance Connect"**
5. Click **"Connect"**
6. Se abre una terminal en el navegador - ¡sin necesidad de SSH!

## ✅ Señales de que SSH funciona correctamente

Cuando SSH funcione bien, verás algo como:

```
Welcome to Ubuntu 24.04.3 LTS
...
ubuntu@ip-172-31-67-180:~$
```

**NOTA:** Verás `ubuntu@` seguido del prompt, NO un login prompt.

## 🚫 Lo que NO deberías ver

Si ves:
- `ip-172-31-67-180 login:`
- `Password:`

Significa que NO estás conectado vía SSH, sino que estás en una consola serial.

## 💡 Recomendación

**Para evitar problemas, usa EC2 Instance Connect:**
- No requiere configuración
- No necesitas el archivo .pem
- Funciona directamente desde el navegador
- Es igual de potente que SSH

