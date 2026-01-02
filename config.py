from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "CloudDeploy API"
    DATABASE_URL: str = "postgresql://user:password@localhost/clouddeploy_db"
    SECRET_KEY: str = "your-super-secret-key-change-this-in-prod"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
