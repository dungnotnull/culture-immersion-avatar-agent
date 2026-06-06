import edge_tts
import asyncio
from src.core.logger import logger

class TTSEngine:
    def __init__(self, voice="en-US-GuyNeural"):
        self.voice = voice

    async def speak(self, text: str, output_path: str = "assets/temp_speech.mp3"):
        logger.info(f"Generating TTS for: {text}")
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.Save(output_path)
        # In a real run, we would then play this audio file
