"""Application configuration using Pydantic settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # API
    api_title: str = "AI Interview Platform"
    api_version: str = "v1"
    api_prefix: str = "/api/v1"
    debug: bool = False
    
    # Gemini API
    gemini_api_key: str
    gemini_model_interviewer: str = "gemini-1.5-flash"
    gemini_model_judge: str = "gemini-1.5-pro"
    gemini_max_retries: int = 3
    gemini_timeout: int = 30
    
    # Database
    database_url: Optional[str] = None  # Will use in-memory for Phase 1
    redis_url: str = "redis://localhost:6379/0"
    
    # LiveKit (Phase 2)
    livekit_url: Optional[str] = None
    livekit_api_key: Optional[str] = None
    livekit_api_secret: Optional[str] = None
    
    # STT/TTS (Phase 2)
    deepgram_api_key: Optional[str] = None
    elevenlabs_api_key: Optional[str] = None
    
    # Docker Sandbox
    docker_network_mode: str = "none"
    docker_mem_limit: str = "512m"
    docker_cpu_quota: int = 100000
    docker_pids_limit: int = 64
    execution_timeout: int = 5
    max_runs_per_interview: int = 10
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    
    # Monitoring
    sentry_dsn: Optional[str] = None
    prometheus_port: int = 9090


settings = Settings()

