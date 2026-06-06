from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "TuTienAnhNgu"
    DEBUG: bool = False
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
