from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "TuTienAnhNgu"
    DEBUG: bool = False
    DATABASE_URL: str

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
