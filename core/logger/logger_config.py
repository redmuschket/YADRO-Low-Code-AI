from dataclasses import dataclass, field
from typing import Dict, Any
from pathlib import Path
import logging
import os


@dataclass
class LoggerConfig:
    yaml_config: Dict[str, Any] = field(default_factory=dict)

    logs_dir: str = field(default_factory=lambda: os.getenv('LOG_DIR', './logs'))
    debug: bool = field(default_factory=lambda: os.getenv('DEBUG', 'False').lower() == 'true')

    def __post_init__(self):
        # Basic settings
        self.file_system = self.yaml_config.get('file_system', 'system.log')
        self.file_user = self.yaml_config.get('file_user', 'user.log')
        self.max_bytes = int(self.yaml_config.get('max_bytes', 10485760))  # 10MB
        self.backup_count = int(self.yaml_config.get('backup_count', 5))
        self.encoding = self.yaml_config.get('encoding', 'utf-8')

        # Formats and levels
        self.system_format = self.yaml_config.get('system_format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_level = self.yaml_config.get('file_level', 'INFO')
        self.console_level = self.yaml_config.get('console_level', 'DEBUG' if self.debug else 'INFO')

        # Creating a folder of logs
        self.path_dir = Path(self.logs_dir)
        self.path_dir.mkdir(exist_ok=True, parents=True)

    def get_log_file_path(self, log_type: str = 'system') -> Path:
        """Returns the full path to the log file"""
        filename = self.file_system if log_type == 'system' else self.file_user
        return self.path_dir / filename

    @property
    def log_level(self) -> bool:
        """Turns the string level into a logging constant"""
        return logging.DEBUG if self.debug else logging.INFO
