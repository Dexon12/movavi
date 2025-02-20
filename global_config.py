from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )
    
    URL: str = "https://sso-auth.movavi.id/v2/auth/check-user-exist"
    CSV_FILE_NAME: str = "data_for_parse.csv"
    RESULT_FILE_NAME: str = "result.json"
    MAX_INSTANCES: int = 3

    
settings = Settings()  # type: ignore
