from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import APP_TITLE, DATABASE_URL


class Settings(BaseSettings):
    app_title: str = APP_TITLE
    database_url: str = DATABASE_URL
    model_config = SettingsConfigDict(env_file='.env')
    secret: str = 'SECRET'

    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = "https://accounts.google.com/o/oauth2/auth"
    token_uri: Optional[str] = "https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = 'example@email.ru'


settings = Settings()