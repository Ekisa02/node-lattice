from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./node_lattice.sqlite"
    WEB3_HTTP_PROVIDER: str = "http://localhost:8545"
    MODEL_PATH: str = "./models/sample_model.pt"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()
