"""Test rápido para verificar que la voz Kelly Ortiz funcione"""
import asyncio
from voice_synthesizer import VoiceSynthesizer
from config import settings
from loguru import logger

async def test_voice():
    """Probar síntesis de voz"""
    logger.info("🧪 Iniciando test de voz...")
    logger.info(f"Voice ID configurado: {settings.voice_bot}")
    
    synthesizer = VoiceSynthesizer()
    await synthesizer.initialize()
    
    test_text = "Hola soy Kelly Ortiz, tu asesora de bancolombia en que puedo ayudarte hoy?"
    logger.info(f"📝 Generando audio para: '{test_text}'")
    
    try:
        audio_bytes = await synthesizer.text_to_speech(test_text, "test_audio.mp3")
        logger.info(f"✅ Audio generado exitosamente: {len(audio_bytes)} bytes")
        logger.info(f"📁 Archivo guardado en: audio_cache/test_audio.mp3")
        return True
    except Exception as e:
        logger.error(f"❌ Error generando audio: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_voice())
    if result:
        print("\n✅ TEST EXITOSO - La voz Kelly Ortiz funciona correctamente")
    else:
        print("\n❌ TEST FALLIDO - Revisa la API key de ElevenLabs o el Voice ID")
