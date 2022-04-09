from pydantic import BaseSettings


class Settings(BaseSettings):
    env: str
    app_name: str = "Passbird Api"
    db_user: str
    db_password: str
    db_host: str

    class Config:
        env_file = ".env"
