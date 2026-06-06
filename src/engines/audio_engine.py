import abc
from typing import Optional
from src.core.logger import logger

class AudioEngine(abc.ABC):
    @abc.abstractmethod
    def start_capture(self):
        pass

    @abc.abstractmethod
    def stop_capture(self):
        pass

    @abc.abstractmethod
    def transcribe(self, audio_data) -> Optional[str]:
        pass

class WhisperAudioEngine(AudioEngine):
    def __init__(self, model_size="large-v3"):
        self.model_size = model_size
        self.model = None # Mocked: would be transformers.pipeline("automatic-speech-recognition")
        logger.info(f"WhisperAudioEngine initialized with model {model_size} (Mocked)")

    def start_capture(self):
        logger.info("Starting system audio capture (Mocked)")

    def stop_capture(self):
        logger.info("Stopping system audio capture (Mocked)")

    def transcribe(self, audio_data) -> Optional[str]:
        # Mock implementation for Phase 0
        return "Mocked transcribed text from audio"
