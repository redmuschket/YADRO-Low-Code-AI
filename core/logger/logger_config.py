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
        self.system_format = self.yaml_config.get(
            'system_format',
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.user_format = self.yaml_config.get(
            'user_format',
            '%(asctime)s - %(levelname)s - %(message)s'
        )

        self.file_level_str = self.yaml_config.get('file_level', 'INFO')
        self.console_level_str = self.yaml_config.get(
            'console_level',
            'DEBUG' if self.debug else 'INFO'
        )
        self.root_level_str = self.yaml_config.get(
            'root_level',
            'DEBUG' if self.debug else 'INFO'
        )
        self.werkzeug_level_str = self.yaml_config.get('werkzeug_level', 'ERROR')

        self.file_level = self._level_to_int(self.file_level_str)
        self.console_level = self._level_to_int(self.console_level_str)
        self.root_level = self._level_to_int(self.root_level_str)
        self.werkzeug_level = self._level_to_int(self.werkzeug_level_str)

    @staticmethod
    def _level_to_int(level_str: str) -> int:
        """Converts the string logging level to the logging constant."""
        level_str = level_str.upper()
        if level_str == 'DEBUG':
            return logging.DEBUG
        elif level_str == 'INFO':
            return logging.INFO
        elif level_str == 'WARNING':
            return logging.WARNING
        elif level_str == 'ERROR':
            return logging.ERROR
        elif level_str == 'CRITICAL':
            return logging.CRITICAL
        else:
            return logging.INFO

    def get_system_log_path(self) -> Path:
        """The full path to the system log file."""
        if isinstance(self.logs_dir, str):
            log_dir = Path(self.logs_dir)
        else:
            log_dir = self.logs_dir
        return log_dir / self.file_system

    def get_user_log_path(self) -> Path:
        """The full path to the user's log file."""
        if isinstance(self.logs_dir, str):
            log_dir = Path(self.logs_dir)
        else:
            log_dir = self.logs_dir
        return log_dir / self.file_user
