import os
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str = "4000"
    DB_NAME: str = "moonshine_ballad"

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @property
    def DATABASE_URL(self) -> str:
        password_encoded = quote_plus(self.DB_PASSWORD)
        return (
            f"mysql+pymysql://{self.DB_USER}:{password_encoded}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            f"?ssl_ca=/etc/ssl/certs/ca-certificates.crt"
        )

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()