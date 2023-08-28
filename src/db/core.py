from pydantic import AnyHttpUrl, BaseSettings, HttpUrl, validator
from typing import List, Optional, Union
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.environ.get("DATABASE_URL")

    BUCKET_NAME: str = os.environ.get("BUCKET_NAME")
    AWS_ACCESS_KEY: str = os.environ.get("AWS_ACCESS_KEY")
    AWS_SECRET_KEY: str = os.environ.get("AWS_SECRET_KEY")
    BUCKET_REGION: str = os.environ.get("BUCKET_REGION")

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        os.environ.get("URL_ONE"),
        os.environ.get("URL_TWO"),
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "FastAPI Image S3"
    SENTRY_DSN: Optional[HttpUrl] = None

    class Config:
        case_sensitive = True


settings = Settings()
