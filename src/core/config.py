from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    OLLAMA_HOST: str = "http://localhost:11434"

    # App Settings
    APP_NAME: str = "Culture Immersion Avatar"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # UI Settings
    OVERLAY_OPACITY: float = 0.8
    OVERLAY_DURATION: int = 8  # seconds
    
    # Model paths (Skeletons for later)
    WHISPER_MODEL_SIZE: str = "large-v3"
    NER_MODEL_NAME: str = "dslim/bert-base-NER"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
