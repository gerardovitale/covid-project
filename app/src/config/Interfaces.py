from abc import ABC, abstractmethod

from src.config.AppConfig import SparkConfig, MongoConfig
from src.resources.Singleton import Singleton


class ConfigurationInterface(ABC, metaclass=Singleton):
    APP_NAME: str
    SERVICE_NAME: str
    DEFAULT_PORT: int


class ConfigLoaderInterface(ABC):

    @classmethod
    @abstractmethod
    def load_config_file(cls, config_file_path: str) -> dict:
        pass

    @classmethod
    @abstractmethod
    def load_spark_config(cls, config: SparkConfig, config_file_path: str) -> SparkConfig:
        pass

    @classmethod
    @abstractmethod
    def load_mongo_config(cls, config: MongoConfig, config_file_path: str) -> MongoConfig:
        pass
