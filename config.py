from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ollama_url : str
    ollama_chat_model: str
    ollama_embedding_model: str
    chroma_db_path: str
    ollama_embedding_url: str
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
