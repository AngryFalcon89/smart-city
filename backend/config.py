from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "mongodb+srv://BilalZaidi:HFaYYcOVxgbOQDyA@cluster0.narqn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()