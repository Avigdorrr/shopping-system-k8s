from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Kafka Configuration
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC: str = "purchases"

    # Management API Configuration
    MANAGEMENT_API_URL: str = "http://localhost:8080"

    # Logging Configuration
    LOG_LEVEL: str = "INFO"


settings = Settings()
