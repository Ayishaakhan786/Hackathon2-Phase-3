from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    database_url: str = "sqlite:///./test.db"

    # OpenAI settings
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"

    # MCP settings
    mcp_server_url: Optional[str] = None
    mcp_api_key: Optional[str] = None

    # Application settings
    app_name: str = "AI Agent Runner"
    app_version: str = "0.1.0"
    debug: bool = False

    # Rate limiting
    rate_limit_per_minute: int = 100

    # Conversation settings
    max_message_length: int = 10000  # Maximum length of a message in characters
    
    # Server settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "info"

    class Config:
        env_file = ".env"


settings = Settings()