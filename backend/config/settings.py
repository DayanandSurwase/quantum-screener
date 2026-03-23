from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    groq_api_key: str
    model_name: str = "llama-3.3-70b-versatile"
    port: int = 8000  

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",            
        protected_namespaces=()   
    )

settings = Settings()