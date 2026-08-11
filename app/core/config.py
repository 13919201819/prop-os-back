from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "propOS Engine API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "propos_super_secret_jwt_key_min_32_characters_long_for_azure_prod"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    ALGORITHM: str = "HS256"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:hzmnhsixmvdgthykfsxn@db.hzmnhsixmvdgthykfsxn.supabase.co:5432/postgres"
    
    # CORS
    ALLOWED_ORIGINS: Union[str, List[str]] = "*"

    # Brevo Transactional Email Integration
    BREVO_API_KEY: str = ""
    BREVO_FROM_EMAIL: str = "noreply@themistrai.com"
    BREVO_FROM_NAME: str = "PropOS"

    @property
    def cors_origins(self) -> List[str]:
        if isinstance(self.ALLOWED_ORIGINS, str):
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]
        return self.ALLOWED_ORIGINS

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"

settings = Settings()
