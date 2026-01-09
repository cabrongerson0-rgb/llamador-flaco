"""
Servidor FastAPI para webhooks de Twilio
Patrón: Template Method - Estructura común para respuestas TwiML
"""
from fastapi import FastAPI, Request, Form
from fastapi.responses import Response, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from typing import Optional
from twilio.twiml.voice_response import VoiceResponse, Gather
import asyncio
import os
from pathlib import Path


# Constantes
AUDIO_DIR = Path("audio_cache")
TIMEOUT_SECONDS = 5.0
DEFAULT_LANGUAGE = 'es-CO'
DEFAULT_VOICE = 'Polly.Mia'

# Inicializar directorio de audio
AUDIO_DIR.mkdir(exist_ok=True)

# FastAPI app
app = FastAPI(title="Voice Caller Webhook Server")

# Referencia global al bot
caller_bot = None


def set_caller_bot(bot) -> None:
    """Establecer referencia al bot principal"""
    global caller_bot
    caller_bot = bot
    logger.info("✅ CallerBot configurado")


def create_error_response(message: str) -> Response:
    """
    Crear respuesta TwiML de error
    Patrón: Factory Method
    """
    response = VoiceResponse()
    response.say(message, language=DEFAULT_LANGUAGE, voice=DEFAULT_VOICE)
    response.hangup()
    return Response(content=str(response), media_type="application/xml")


# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware de logging"""
    logger.info(f"🌐 {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"📤 Status: {response.status_code}")
    return response


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "ok",
        "service": "Voice Caller",
        "bot_ready": caller_bot is not None
    }


@app.get("/test")
async def test_endpoint():
    """Endpoint de prueba"""
    return {"test": "success", "message": "Webhook OK"}


@app.get("/audio/{filename}")
async def serve_audio(filename: str):
    """Servir archivos de audio"""
    audio_path = AUDIO_DIR / filename
    if audio_path.exists():
        return FileResponse(str(audio_path), media_type="audio/mpeg")
    logger.error(f"❌ Audio no encontrado: {filename}")
    return Response(content="Not found", status_code=404)



@app.post("/voice/incoming")
async def handle_incoming_call(request: Request):
    """Webhook para llamadas entrantes"""
    try:
        form_data = await request.form()
        call_sid = form_data.get('CallSid')
        from_number = form_data.get('From', 'Unknown')
        to_number = form_data.get('To', 'Unknown')
        
        logger.info(f"📞 INCOMING - SID: {call_sid} | FROM: {from_number}")
        
        # Validaciones
        if not caller_bot:
            logger.error("🚨 caller_bot NO INICIALIZADO")
            return create_error_response(
                "Disculpa, el sistema no está disponible. Intenta más tarde. Hasta luego."
            )
        
        if not call_sid:
            logger.error("🚨 Sin CallSid")
            return create_error_response("Error técnico. Intenta nuevamente. Hasta luego.")
        
        if not hasattr(caller_bot, 'voip_manager') or not caller_bot.voip_manager:
            logger.error("🚨 voip_manager NO INICIALIZADO")
            return create_error_response("Sistema no disponible. Intenta después. Hasta luego.")
        
        # Procesar llamada con timeout
        try:
            twiml = await asyncio.wait_for(
                caller_bot.voip_manager.handle_incoming_call(call_sid),
                timeout=TIMEOUT_SECONDS
            )
            logger.info(f"✅ TwiML generado: {len(twiml)} chars")
            return Response(content=twiml, media_type="application/xml")
        
        except asyncio.TimeoutError:
            logger.error(f"⏱️ TIMEOUT procesando {call_sid[:8]}")
            # Fallback: saludo simple
            response = VoiceResponse()
            gather = Gather(
                input='speech dtmf',
                language=DEFAULT_LANGUAGE,
                timeout=3,
                speechTimeout='auto',
                action='/voice/process_speech',
                method='POST',
                hints='sí, no, claro, bueno, listo, hola, aló'
            )
            gather.say("Hola buenas. ¿Me escuchas bien?", language=DEFAULT_LANGUAGE, voice=DEFAULT_VOICE)
            response.append(gather)
            response.redirect('/voice/process_speech')
            return Response(content=str(response), media_type="application/xml")
    
    except Exception as e:
        logger.error(f"🚨 ERROR webhook: {e}", exc_info=True)
        return create_error_response(
            "Ha ocurrido un error. Disculpa las molestias. Hasta luego."
        )



@app.post("/voice/process_speech")
async def process_speech(
    request: Request,
    SpeechResult: Optional[str] = Form(None),
    Digits: Optional[str] = Form(None),
    CallSid: Optional[str] = Form(None)
):
    """Webhook para procesar voz y DTMF"""
    try:
        # Determinar tipo de entrada
        user_input = Digits or SpeechResult
        input_type = "DTMF" if Digits else "VOZ"
        
        if Digits:
            logger.info(f"⌨️ DTMF - Call: {CallSid}, Digits: {Digits}")
        elif SpeechResult:
            logger.info(f"🎤 VOZ - Call: {CallSid}, Text: {SpeechResult}")
        
        # Validaciones
        if not CallSid:
            logger.error("🚨 Sin CallSid")
            return create_error_response("Error procesando respuesta. Hasta luego.")
        
        if not user_input or user_input.strip() == "":
            logger.warning(f"⚠️ Sin entrada para {CallSid}")
            if caller_bot:
                return Response(
                    content=await caller_bot.voip_manager.generate_followup_question(CallSid),
                    media_type="application/xml"
                )
            return create_error_response("No recibimos tu respuesta. Hasta luego.")
        
        # Procesar entrada
        if caller_bot:
            twiml = await caller_bot.voip_manager.handle_speech_input(
                CallSid,
                user_input,
                input_type
            )
            return Response(content=twiml, media_type="application/xml")
        
        return create_error_response("Sistema no disponible. Hasta luego.")
    
    except Exception as e:
        logger.error(f"Error procesando entrada: {e}", exc_info=True)
        return create_error_response(
            "Error procesando tu respuesta. Disculpa. Hasta luego."
        )



@app.post("/voice/status")
async def call_status_callback(request: Request):
    """Webhook para actualizaciones de estado"""
    try:
        form_data = await request.form()
        call_sid = form_data.get('CallSid')
        call_status = form_data.get('CallStatus')
        
        logger.info(f"📊 Status - Call: {call_sid}, Status: {call_status}")
        
        if caller_bot:
            await caller_bot.voip_manager.handle_call_status(call_sid, call_status)
        
        return {"status": "ok"}
    
    except Exception as e:
        logger.error(f"Error en status callback: {e}")
        return {"status": "error", "message": str(e)}


@app.post("/voice/recording")
async def recording_callback(request: Request):
    """Webhook para grabaciones completadas"""
    try:
        form_data = await request.form()
        call_sid = form_data.get('CallSid')
        recording_url = form_data.get('RecordingUrl')
        recording_duration = form_data.get('RecordingDuration')
        
        logger.info(f"🎙️ Grabación - Call: {call_sid}, Duración: {recording_duration}s")
        logger.info(f"📥 URL: {recording_url}")
        
        return {"status": "ok"}
    
    except Exception as e:
        logger.error(f"Error en recording callback: {e}")
        return {"status": "error", "message": str(e)}
