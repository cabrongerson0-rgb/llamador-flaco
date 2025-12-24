"""Síntesis de voz optimizada - Solo ElevenLabs"""
from elevenlabs import generate, set_api_key, Voice, VoiceSettings
from loguru import logger
from config import settings
import os


class VoiceSynthesizer:
    """Generador de voz con ElevenLabs - Rachel"""
    
    def __init__(self):
        self.voice_id = settings.voice_bot
        self.audio_dir = "audio_cache"
        self._settings = None
    
    async def initialize(self):
        """Inicializar ElevenLabs"""
        set_api_key(settings.elevenlabs_api_key)
        os.makedirs(self.audio_dir, exist_ok=True)
        
        self._settings = VoiceSettings(
            stability=settings.voice_stability,
            similarity_boost=settings.voice_similarity,
            style=settings.voice_style,
            use_speaker_boost=settings.voice_speaker_boost
        )
        
        logger.info(f"✅ Voz Kelly Ortiz ({self.voice_id}) lista - Ultra realista (ElevenLabs)")
    
    async def text_to_speech(self, text: str, filename: str = None) -> bytes:
        """Generar audio con modelo turbo v2.5 (más rápido y natural)"""
        try:
            logger.info(f"🎤 Generando audio con voz {self.voice_id}...")
            audio = generate(
                text=text,
                voice=Voice(voice_id=self.voice_id, settings=self._settings),
                model="eleven_turbo_v2_5"  # Modelo más rápido y natural
            )
            
            audio_bytes = audio if isinstance(audio, bytes) else b''.join(audio)
            
            if filename:
                filepath = os.path.join(self.audio_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(audio_bytes)
                logger.info(f"💾 Audio guardado: {filepath}")
            
            return audio_bytes
        except Exception as e:
            logger.error(f"❌ Error en text_to_speech: {e}")
            logger.error(f"Voice ID usado: {self.voice_id}")
            raise
