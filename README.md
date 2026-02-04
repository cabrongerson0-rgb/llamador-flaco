# Sistema de Llamadas Telefónicas con IA

Sistema automatizado de llamadas telefónicas con inteligencia artificial, síntesis de voz y gestión VoIP.

## 🚀 Deploy en Railway

### Variables de Entorno Requeridas

Configura estas variables en Railway:

```env
# Bot de Telegram
TELEGRAM_BOT_TOKEN=tu_token_bot

# ElevenLabs (Síntesis de Voz)
ELEVENLABS_API_KEY=tu_api_key
VOICE_BOT=E5HSnXz7WUojYdJeUcng

# OpenAI
OPENAI_API_KEY=tu_api_key

# Twilio (VoIP)
TWILIO_ACCOUNT_SID=tu_account_sid
TWILIO_AUTH_TOKEN=tu_auth_token
TWILIO_PHONE_NUMBER=+1234567890
TWILIO_WEBHOOK_URL=tu_webhook_url

# Webhook
WEBHOOK_URL=https://tu-dominio.railway.app
WEBHOOK_PORT=8000
```

### Pasos para Deploy

1. Conecta este repositorio en Railway
2. Configura las variables de entorno
3. Railway detectará automáticamente el `Procfile` y `railway.json`
4. El sistema se desplegará automáticamente

## 📋 Características

- ✅ Bot de Telegram para control
- ✅ Llamadas VoIP con Twilio
- ✅ Síntesis de voz con ElevenLabs
- ✅ IA conversacional con OpenAI
- ✅ Gestión de llamadas en tiempo real
- ✅ Webhook para recepción de llamadas

## 🛠️ Tecnologías

- Python 3.14
- python-telegram-bot 21.10
- Twilio
- ElevenLabs
- OpenAI
- FastAPI
- Uvicorn

## 📞 Uso

Una vez desplegado, inicia el bot de Telegram y usa los comandos disponibles para realizar llamadas.

## 🔧 Desarrollo Local

```bash
pip install -r requirements.txt
python main.py
```

## 📝 Notas

- Asegúrate de tener ngrok o un webhook público configurado para desarrollo local
- Railway proporciona automáticamente un dominio público para producción
