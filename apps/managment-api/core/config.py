from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Kafka Configuration
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC: str = "purchases"
    KAFKA_GROUP_ID: str = "management-api-group"

    # Mongo Configuration
    MONGO_HOSTNAME: str = "localhost"
    MONGO_PORT: str = "27017"
    MONGO_DB_NAME: str = "shopping"
    MONGO_COLLECTION_NAME: str = "purchases"

    # Logging Configuration
    LOG_LEVEL: str = "INFO"


settings = Settings()
