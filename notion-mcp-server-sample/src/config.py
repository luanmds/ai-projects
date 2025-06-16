"""
Configuration management for the MCP server.
"""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Server settings
    server_name: str = Field(default="Notion MCP Server", description="Name of the MCP server")
    server_version: str = Field(default="0.1.0", description="Version of the MCP server")
    
    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string"
    )
    
    # Notion API settings
    notion_api_key: Optional[str] = Field(default=None, description="Notion API key")
    notion_version: str = Field(default="2022-06-28", description="Notion API version")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
