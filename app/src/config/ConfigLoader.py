import json

from src.config.AppConfig import SparkConfig, MongoConfig
from src.config.Interfaces import ConfigLoaderInterface


class ConfigLoader(ConfigLoaderInterface):
    @classmethod
    def load_config_file(cls, config_file_path: str) -> dict:
        with open(config_file_path) as json_file:
            config_dict = json.load(json_file)
            return config_dict

    @classmethod
    def load_spark_config(cls, config: SparkConfig, config_file_path: str) -> SparkConfig:
        pass

    @classmethod
    def load_mongo_config(cls, config: MongoConfig, config_file_path: str) -> MongoConfig:
        pass
