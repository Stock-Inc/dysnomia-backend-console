from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Db(BaseModel):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME: str

    @computed_field
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"

class Bot(BaseModel):
    TOKEN: str

class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_nested_delimiter="_",
    )

    DB: Db
    BOT: Bot

app_config = Config()