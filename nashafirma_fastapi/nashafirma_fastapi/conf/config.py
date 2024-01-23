from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    # secret_key: str
    # algorithm: str
    # mail_username: str
    # mail_password: str
    # mail_from: str
    # mail_port: int
    # mail_server: str
    # redis_host: str
    # redis_port: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
