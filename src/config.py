from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent

class EnvData(BaseSettings):

    DB_URl: str
    DB_URl_ASYNC: str
    model_config = SettingsConfigDict(env_file='.env.local', env_file_encoding="utf-8")


class Config(BaseModel):

    env_data:EnvData = EnvData()

    
config = Config()