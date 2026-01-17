from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Kafka Configuration
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC: str = "purchases"

    # Management API Configuration
    MANAGEMENT_API_ENDPOINT: str = "localhost:8080"

    # App Configuration
    LOG_LEVEL: str = "INFO"
    APP_PORT: int = 8081



settings = Settings()
