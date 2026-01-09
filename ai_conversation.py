"""
Módulo de conversación con IA usando OpenAI GPT
Gestiona interacciones naturales con memoria de contexto
"""
from openai import AsyncOpenAI
from loguru import logger
from config import settings
from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class ConversationMessage:
    """Mensaje en conversación"""
    role: str
    content: str


class AIConversation:
    """
    Gestor de conversaciones IA con contexto persistente
    Implementa patrón Strategy para diferentes tipos de prompt
    """
    
    MAX_HISTORY = 24  # 12 intercambios usuario-IA
    MAX_WORDS = 15    # Máximo palabras por respuesta
    
    BASE_PROMPT = """Eres LLAMADOR EL LOBO HR, asesora profesional colombiana.

🎯 PERSONALIDAD:
- Profesional, cercana, amable
- Escucha activa, empática
- Natural, conversacional
- Mantén contexto completo
- Lenguaje colombiano: "listo", "perfecto", "claro"

📞 ESTRUCTURA:
1. Inicias: saludo + motivo
2. Escuchas respuesta completa
3. Respondes directo (máx 15 palabras)
4. Preguntas específicas
5. NO repites información

✅ COMUNICACIÓN:
- Confirma: "Perfecto" / "Listo"
- Una pregunta a la vez
- Espera respuesta

🚫 PROHIBIDO:
- Repetir presentación
- Preguntar datos ya dados
- Respuestas robóticas
- Más de 15 palabras"""
    
    def __init__(self):
        """Inicializar cliente OpenAI y estado"""
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.conversations: Dict[str, List[dict]] = {}
        self.custom_instruction: str = ""
    
    @property
    def system_prompt(self) -> str:
        """Construir prompt sistema con instrucción personalizada"""
        if self.custom_instruction:
            return f"{self.BASE_PROMPT}\n\n🎯 ROL:\n{self.custom_instruction}\n\nRECUERDA: Máx {self.MAX_WORDS} palabras."
        return self.BASE_PROMPT
    
    async def get_initial_greeting(self) -> str:
        """Generar saludo inicial"""
        logger.info("🔑 Generando saludo")
        
        if not self.custom_instruction:
            logger.warning("⚠️ Sin instrucción")
            return "Hola, te llamamos de servicio al cliente. ¿Me escuchas?"
        
        try:
            logger.info(f"📝 Instrucción: {len(self.custom_instruction)} chars")
            
            response = await self.client.chat.completions.create(
                model=settings.ai_model,
                messages=[
                    {"role": "system", "content": f"{self.BASE_PROMPT}\n\nROL:\n{self.custom_instruction}"},
                    {"role": "user", "content": "Tú llamas. Hablas PRIMERO. Saludo + origen + motivo. 10-20 palabras."}
                ],
                temperature=settings.ai_temperature,
                max_tokens=settings.ai_max_tokens,
                timeout=settings.ai_timeout
            )
            
            greeting = self._clean_text(response.choices[0].message.content)
            logger.info(f"✅ Saludo: {greeting}")
            return greeting
            
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return "Cordial saludo. ¿Me escuchas bien?"
    
    async def get_response(self, call_sid: str, user_input: str) -> str:
        """Generar respuesta BASADA en lo que el usuario dijo - Contexto extendido"""
        if call_sid not in self.conversations:
            self.conversations[call_sid] = []
        
        # Log para ver qué esIA con contexto"""
        if call_sid not in self.conversations:
            self.conversations[call_sid] = []
        
        logger.info(f"🗣️ Usuario: '{user_input}'")
        self.conversations[call_sid].append({"role": "user", "content": user_input})
        
        try:
            messages = [{"role": "system", "content": self.system_prompt}] + self.conversations[call_sid]
            
            response = await self.client.chat.completions.create(
                model=settings.ai_model,
                messages=messages,
                temperature=settings.ai_temperature,
                max_tokens=settings.ai_max_tokens,
                timeout=settings.ai_timeout,
                presence_penalty=0.7,
                frequency_penalty=0.8
            )
            
            ai_response = self._clean_text(response.choices[0].message.content)
            logger.info(f"🤖 IA: '{ai_response}'")
            
            self.conversations[call_sid].append({"role": "assistant", "content": ai_response})
            
            # Limitar historial
            if len(self.conversations[call_sid]) > self.MAX_HISTORY:
                self.conversations[call_sid] = self.conversations[call_sid][-self.MAX_HISTORY:]
            
            return ai_response
            
        except Exception as e:
            logger.error(f"❌ Error IA: {e}")
            return "¿Qué decías? No te oí bien."
    
    def set_custom_prompt(self, prompt: str) -> None:
        """Configurar prompt personalizado"""
        self.custom_instruction = prompt
        logger.info(f"✅ Prompt: {len(prompt)} chars")
        logger.info(f"📋 {prompt[:100]}...")
    
    def clear_conversation(self, call_sid: str) -> None:
        """Limpiar conversación"""
        if call_sid in self.conversations:
            del self.conversations[call_sid]
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """Limpiar formato de texto"""
        return text.strip().replace('*', '').replace('_', '').replace('"', '').replace('  ', ' ')