from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url:str
    elastic_cloud_id:str
    elastic_API_key:str

    class Config:
        env_file=".env"

settings=Settings()