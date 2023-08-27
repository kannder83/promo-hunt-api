from pydantic import BaseSettings


class Settings(BaseSettings):
    # API
    mode_prod: bool
    debug: bool
    version: str
    dev_url: str
    prod_url: str
    allowed_hosts: list
    workers: int
    prod_port: int
    # DB configuration
    database_hostname: str
    database_port: int
    database_password: str
    database_username: str
    database_web_user: str
    database_web_password: str
    # Email
    email_sender: str
    email_password: str
    #  PLAYWRIGHT
    playwright_headless: bool
    playwright_sandbox: bool
    chunk_size: int
    timeout: int

    class Config:
        env_file = ".env"


settings = Settings()
