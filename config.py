from pydantic_settings import BaseSettings
from scam_master.services.enums.base import StrEnum


class APIConfig(BaseSettings):
    VERSION: str = '1.0.0'
    TITLE: str = 'Scam Master API'
    SUMMARY: str | None = None
    DESCRIPTION: str = 'Bank transfer system API'
    PREFIX: str = '/api'
    IS_VISIBLE: bool = False

    class Config:
        env_prefix = 'API_'
        env_file = '.env'


class AppConfig(BaseSettings):
    PORT: int = 80
    HOST: str = '0.0.0.0'
    DEBUG: bool = False

    class Config:
        env_prefix = 'APP_'
        env_file = '.env'


class LogConfig(BaseSettings):
    class LogLevel(StrEnum):
        debug = 'DEBUG'
        info = 'INFO'
        error = 'ERROR'

    LEVEL: LogLevel = LogLevel.info
    TO_FILE: bool = True
    LOG_DIR: str = 'logs'
    RETENTION: int = 5
    ROTATION: int = 500

    class Config:
        env_prefix = 'LOG_'
        use_enum_values = True
        env_file = '.env'


class Config(BaseSettings):
    api: APIConfig = APIConfig()
    app: AppConfig = AppConfig()
    log: LogConfig = LogConfig()