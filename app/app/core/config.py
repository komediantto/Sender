from typing import Any, Dict, Optional
from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str

    BOT_TOKEN: str
    BOT_ID: int
    ADMIN_ID: int
    GROUP: int

    ASYNC_SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    SYNC_SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SYNC_SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_sync_db_connection(cls, v: Optional[str],
                                    values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True


settings = Settings()
