from pathlib import Path
from typing import Set

import yaml
from dotenv import load_dotenv

from core.db.config_db import ConfigDB
from core.logger.logger import Logger
from core.logger.logger_config import LoggerConfig


class Config:
    NOTIFICATION_UUID_VERSION: int = 7

    def __init__(self, yaml_path: str = "config.yaml", env_file: str = ".env"):
        self.env_path = Path(env_file)
        self.safe_reload_env(env_file)
        with open(yaml_path, "r", encoding="utf-8") as f:
            self.__config = yaml.safe_load(f)
            self.logger = self._setup_logger()
            self.db_config = self._setup_db_config()

    @staticmethod
    def safe_reload_env(env_file: str) -> bool:
        try:
            load_dotenv(env_file)
            print("WARNING: Environment reloaded successfully")
            return True
        except Exception as e:
            print(f"ERROR: Failed to reload environment: {e}")
            return False

    @property
    def storage_dir(self):
        return self.__config["storage"]["storage_dir"]

    def _setup_logger(self) -> Logger:
        logger_config = LoggerConfig(yaml_config=self.__config.get("log", {}))
        logger = Logger.init_logger(logger_config)
        return logger

    def _setup_db_config(self):
        db_config = ConfigDB()
        db_config.yaml_config = self.__config["database"]
        return db_config

