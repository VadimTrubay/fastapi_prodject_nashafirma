from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str = (
        "postgresql+psycopg2://user:password@server:5432/database"
    )
    secret_key: str = "secret"
    algorithm: str = "HS256"
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    redis_host: str
    redis_port: int
    CLOUDINARY_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
