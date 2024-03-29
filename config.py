from pydantic_settings import BaseSettings
from enum import Enum


class StrEnum(str, Enum):
    @classmethod
    def _missing_(cls, value):
        value = value.upper()
        for member in cls:
            if member.upper() == value:
                return member
        return None


class APIConfig(BaseSettings):
    VERSION: str = '1.0.0'
    TITLE: str = 'Scam Master API'
    SUMMARY: str | None = None
    DESCRIPTION: str = 'Bank transfer system API'
    PREFIX: str = '/api'
    IS_VISIBLE: bool = True

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
        debug = 'debug'
        info = 'info'
        error = 'error'

    LEVEL: LogLevel = LogLevel.info
    DIR: str = ''
    RETENTION: int = 5
    ROTATION: int = 100

    class Config:
        env_prefix = 'LOG_'
        use_enum_values = True
        env_file = '.env'


class BrowserConfig(BaseSettings):
    PATH: str = ''
    
    class Config:
        env_prefix = 'BROWSER_'
        env_file = '.env'


class KafkaConfig(BaseSettings):
    BOOTSTRAP_SERVERS: str = 'scam_master_kafka:9092'

    class Config:
        env_prefix = 'KAFKA_'
        env_file = '.env'


class BankConfig(BaseSettings):
    URL: str
    TIMEOUT: int


class TinkoffConfig(BankConfig):
    URL: str = 'https://www.tinkoff.ru/cardtocard/'
    TIMEOUT: int = 600
        
    class Config:
        env_prefix = 'BANK_TINKOFF_'
        env_file = '.env'


class OtpbankConfig(BankConfig):
    URL: str = 'https://www.otpbank.ru/p2p/'
    TIMEOUT: int = 600
        
    class Config:
        env_prefix = 'BANK_OTPBANK_'
        env_file = '.env'


class RshbankConfig(BankConfig):
    URL: str = 'https://old.rshb.ru/p2p/'
    TIMEOUT: int = 600
        
    class Config:
        env_prefix = 'BANK_RSHBANK'
        env_file = '.env'


class BanksConfig(BaseSettings):
    tinkoff: TinkoffConfig = TinkoffConfig()
    otp: OtpbankConfig = OtpbankConfig()
    rsh: RshbankConfig = RshbankConfig()


class Config(BaseSettings):
    api: APIConfig = APIConfig()
    app: AppConfig = AppConfig()
    log: LogConfig = LogConfig()
    banks: BanksConfig = BanksConfig()
    kafka: KafkaConfig = KafkaConfig()
    browser: BrowserConfig = BrowserConfig()
