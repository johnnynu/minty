"""Application configuration settings"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    app_name: str = "Minty API"
    env: str = "development"
    debug: bool = True

    # Database
    database_url: str

    # Clerk Authentication
    clerk_secret_key: str
    clerk_publishable_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


settings = Settings() # type: ignore
