from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_username: str = ''
    database_hostname: str = ''
    database_port: str = ''
    database_password: str = ''
    database_name: str = ''
    secret_key: str = ''
    algorithm: str = ''
    access_token_expire_minutes: int = 0
    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
