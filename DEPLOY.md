# 🚀 GUÍA RÁPIDA DE DESPLIEGUE - KELLY ORTIZ

## ✅ PASO 1: Subir a GitHub

Abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
# 1. Ir a la carpeta del proyecto
cd C:\Users\Hansel\Desktop\ARES_ELLOBOHR

# 2. Inicializar git (si no está)
git init

# 3. Configurar repositorio remoto
git remote add origin https://github.com/hanselrosales255/software-llamador-rafasocios.git

# 4. Agregar archivos
git add .

# 5. Commit
git commit -m "Sistema Kelly Ortiz optimizado - Tiempo real"

# 6. Subir a GitHub
git push -u origin main
```

**Si te pide credenciales de GitHub:**
- Usuario: tu_usuario_de_github
- Contraseña: usa un **Personal Access Token** (no tu contraseña)
  - Genera uno en: https://github.com/settings/tokens
  - Permisos necesarios: `repo` (todos los permisos de repositorio)

---

## ✅ PASO 2: Desplegar en Railway

### 2.1 Crear Proyecto en Railway

1. Ve a: https://railway.app/
2. Haz clic en **"Login"** → Login con GitHub
3. Haz clic en **"New Project"**
4. Selecciona **"Deploy from GitHub repo"**
5. Busca: `hanselrosales255/software-llamador-rafasocios`
6. Haz clic en el repositorio

Railway comenzará a desplegar automáticamente.

### 2.2 Configurar Variables de Entorno

1. En Railway, haz clic en tu proyecto
2. Ve a la pestaña **"Variables"**
3. Haz clic en **"New Variable"** para cada una:

```env
TELEGRAM_BOT_TOKEN=tu_token_de_botfather
TELEGRAM_ADMIN_IDS=tu_telegram_user_id
TWILIO_ACCOUNT_SID=tu_twilio_sid
TWILIO_AUTH_TOKEN=tu_twilio_token
TWILIO_PHONE_NUMBER=+tu_numero_twilio
OPENAI_API_KEY=sk-tu_openai_key
ELEVENLABS_API_KEY=tu_elevenlabs_key
WEBHOOK_URL=https://tu-dominio.railway.app
WEBHOOK_PORT=8000
```

### 2.3 Generar Dominio Público

1. En Railway, ve a **"Settings"**
2. Busca **"Networking"** o **"Public Networking"**
3. Haz clic en **"Generate Domain"**
4. Copia el dominio (ejemplo: `llamador-production-a1b2.up.railway.app`)
5. Ve a **"Variables"**
6. Edita `WEBHOOK_URL` y pega: `https://tu-dominio-copiado.up.railway.app`
7. Guarda

### 2.4 Redeployar

1. Haz clic en la pestaña **"Deployments"**
2. Haz clic en los 3 puntos del deployment activo
3. Selecciona **"Redeploy"**
4. Espera 1-2 minutos

---

## ✅ PASO 3: Configurar Twilio

### 3.1 Abrir Twilio Console

1. Ve a: https://console.twilio.com/
2. Login con tu cuenta
3. Ve a **"Phone Numbers"** → **"Manage"** → **"Active Numbers"**
4. Haz clic en tu número de teléfono

### 3.2 Configurar Webhooks

En la sección **"Voice & Fax"**:

**A CALL COMES IN:**
- Webhook: `https://tu-dominio.railway.app/webhook/voice`
- HTTP: `POST`

**STATUS CALLBACK URL:**
- Webhook: `https://tu-dominio.railway.app/webhook/status`  
- HTTP: `POST`

**IMPORTANTE:** Reemplaza `tu-dominio.railway.app` con tu dominio real de Railway.

### 3.3 Guardar

Haz clic en **"Save"** al final de la página.

---

## ✅ PASO 4: Verificar que Funciona

### 4.1 Ver Logs en Railway

1. En Railway, ve a **"Deployments"**
2. Haz clic en el deployment activo
3. Haz clic en **"View Logs"**

**Deberías ver:**
```
✅ Bot de Telegram iniciado
✅ Cliente Twilio inicializado correctamente
✅ Voz Kelly Ortiz (7h1bGU3p2v8oSDwv8Ivg) lista
🌐 Iniciando servidor webhook en puerto 8000
✅ Sistema activo
```

### 4.2 Probar el Bot de Telegram

1. Abre Telegram
2. Busca tu bot
3. Envía: `/start`

**Deberías ver:**
```
📞 LLAMADOR KELLY ORTIZ

🎯 COMANDOS:
/llamar +57312... - Hacer llamada
/masivo +num1 +num2 - Llamadas múltiples
/activas - Ver llamadas activas
/colgar - Colgar todas
...
```

### 4.3 Hacer una Llamada de Prueba

```
/instruccion Eres Kelly Ortiz, asesora profesional. Saluda brevemente y pregunta cómo puedes ayudar. Máximo 8 palabras.
/llamar +573012345678
```

Reemplaza con tu número de teléfono.

---

## 🎯 CONFIGURACIÓN PARA BANCOLOMBIA TRICOLOR

Si quieres usar el protocolo Bancolombia, envía este comando en Telegram:

```
/instruccion Eres Kelly Ortiz, asesora del área de bloqueos y seguridad de Bancolombia. Realiza validación de seguridad biométrica. Saluda: "Hola, le habla Kelly Ortiz de Bancolombia. Me comunico con el señor? Cómo está?". Explica motivo: "El sistema reportó movimiento sospechoso. Necesitamos validación de seguridad". Pregunta disponibilidad. Solicita descarga app SOY YO. Guía paso a paso. Máximo 8 palabras por turno. Natural, profesional, colombiana.
```

Luego haz la llamada:
```
/llamar +573012345678
```

---

## ⚠️ SOLUCIÓN DE PROBLEMAS

### El bot no responde
- ✅ Verifica `TELEGRAM_BOT_TOKEN` en Railway
- ✅ Verifica que tu ID esté en `TELEGRAM_ADMIN_IDS`
- ✅ Mira los logs en Railway

### Las llamadas no conectan
- ✅ Verifica webhook en Twilio (debe ser HTTPS)
- ✅ Verifica que el dominio de Railway esté correcto
- ✅ Verifica que `TWILIO_PHONE_NUMBER` tenga `+`

### La voz no funciona
- ✅ Verifica `ELEVENLABS_API_KEY` en Railway
- ✅ Verifica que tengas créditos en ElevenLabs
- ✅ La voz Kelly Ortiz es: `7h1bGU3p2v8oSDwv8Ivg`

### Errores en Railway
```powershell
# Ver logs en tiempo real
Railway → Deployments → View Logs

# Si hay error, redeploy:
Deployments → ... → Redeploy
```

---

## 📞 COMANDOS ÚTILES

```
# Llamada simple
/llamar +573012345678

# Llamadas múltiples
/masivo +573012345678 +573098765432

# Ver activas
/activas

# Colgar todas
/colgar

# Cambiar comportamiento
/instruccion Eres Kelly...
```

---

## 🎯 CHECKLIST FINAL

Antes de usar en producción, verifica:

- [ ] Código subido a GitHub
- [ ] Proyecto desplegado en Railway
- [ ] Todas las variables de entorno configuradas
- [ ] Dominio generado en Railway
- [ ] Webhook configurado en Twilio
- [ ] Bot responde en Telegram
- [ ] Llamada de prueba exitosa
- [ ] Voz de Kelly suena bien
- [ ] Respuestas sin delay (<2 segundos)

---

## 💡 TIPS FINALES

1. **Prueba primero**: Haz llamadas de prueba antes de producción
2. **Monitorea**: Revisa logs en Railway periódicamente
3. **Instrucciones claras**: Sé específico con `/instruccion`
4. **Respuestas cortas**: Kelly funciona mejor con respuestas de 5-8 palabras
5. **Créditos**: Revisa tus créditos en ElevenLabs y OpenAI

---

¡Listo! 🎉 Tu sistema Kelly Ortiz está desplegado y funcionando en tiempo real.

**Dominio Railway**: https://tu-dominio.railway.app
**Bot Telegram**: @tu_bot
**Teléfono Twilio**: +tu_numero

---

**¿Problemas?** Revisa los logs en Railway y verifica cada paso.
