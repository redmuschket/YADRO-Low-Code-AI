import os
from pathlib import Path

from config import Config

base_dir = Path(__file__).resolve().parent.parent

config = Config(
    yaml_path=str(base_dir / os.getenv("CONFIG_YAML_PATH", "config.yaml")),
    env_file=str(base_dir / os.getenv("CONFIG_ENV_PATH", ".env")),
)

# logger
logger = config.logger
