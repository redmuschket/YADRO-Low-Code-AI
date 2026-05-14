import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from core.logger.logger_config import LoggerConfig


class Logger:
    """
    Singleton logger class with file rotation and dynamic log level control.
    Handles both console and file logging with different levels.
    """

    _instance: Optional['Logger'] = None
    _handlers_initialized: bool = False
    _force_debug: bool = False

    def __init__(self, logger_config: LoggerConfig):
        self.config = logger_config
        self._info_handler: Optional[RotatingFileHandler] = None
        self._error_handler: Optional[RotatingFileHandler] = None
        self._debug_handler: Optional[RotatingFileHandler] = None
        self._user_handler: Optional[RotatingFileHandler] = None
        self._console_handler: Optional[logging.StreamHandler] = None
        self._setup_logging()

    def _setup_logging(self):
        """
        Initialize logging handlers with rotation.
        Creates separate handlers for info, errors, debug, and console output.
        """
        if Logger._handlers_initialized:
            return

        # Creating a folder of logs
        log_dir = self.config.logs_dir
        if isinstance(log_dir, str):
            log_dir = Path(log_dir)
        log_dir.mkdir(exist_ok=True, parents=True)

        formatter = logging.Formatter(self.config.system_format)

        root_logger = logging.getLogger()

        def make_handler(file_path: Path, level: int, fmt_str: str) -> RotatingFileHandler:
            """Create a rotating file handler with specified level."""
            handler = RotatingFileHandler(
                filename=file_path,
                maxBytes=self.config.max_bytes,
                backupCount=self.config.backup_count,
                encoding=self.config.encoding
            )
            handler.setFormatter(logging.Formatter(fmt_str))
            handler.setLevel(level)
            return handler

        class InfoFilter(logging.Filter):
            """Filter that only passes INFO level messages (not ERROR or above)."""
            def filter(self, record):
                return logging.INFO <= record.levelno < logging.ERROR

        # System handlers (by levels)
        system_path = self.config.get_system_log_path()
        stem = system_path.stem          # "system"
        suffix = system_path.suffix      # ".log"

        # Handler for INFO level messages only
        info_path = log_dir / f"{stem}_info{suffix}"
        self._info_handler = make_handler(info_path, logging.INFO, self.config.system_format)
        self._info_handler.addFilter(InfoFilter())
        root_logger.addHandler(self._info_handler)

        # Handler for ERROR level messages and above
        error_path = log_dir / f"{stem}_errors{suffix}"
        self._error_handler = make_handler(error_path, logging.ERROR, self.config.system_format)
        root_logger.addHandler(self._error_handler)

        # Handler for DEBUG level messages (optional)
        if self.config.debug:
            debug_path = log_dir / f"{stem}_debug{suffix}"
            self._debug_handler = make_handler(debug_path, logging.DEBUG, self.config.system_format)
            root_logger.addHandler(self._debug_handler)

        # User's log
        user_logger = logging.getLogger('user')
        user_logger.setLevel(self.config.file_level)
        user_logger.propagate = False
        self._user_handler = make_handler(
            self.config.get_user_log_path(),
            self.config.file_level,
            self.config.user_format
        )
        user_logger.addHandler(self._user_handler)

        # Console handler for real-time output
        self._console_handler = logging.StreamHandler()
        self._console_handler.setFormatter(formatter)
        self._console_handler.setLevel(self.config.console_level)
        root_logger.addHandler(self._console_handler)

        # Root logger and werkzeug level
        logging.getLogger().setLevel(self.config.root_level)
        logging.getLogger('werkzeug').setLevel(self.config.werkzeug_level)

        Logger._handlers_initialized = True

    def set_log_level(self, level: int) -> None:
        """
        Change the log level for all handlers and the root logger.

        Args:
            level: Log level (logging.DEBUG, logging.INFO, etc.)
        """
        root_logger = logging.getLogger()
        root_logger.setLevel(level)

        # Update console handler level
        if self._console_handler:
            self._console_handler.setLevel(level)

        # Update file handlers levels
        if self._info_handler:
            self._info_handler.setLevel(min(level, logging.INFO))
        if self._error_handler:
            self._error_handler.setLevel(min(level, logging.ERROR))
        if self._debug_handler:
            self._debug_handler.setLevel(level)

        logger = logging.getLogger(__name__)
        logger.info(f"Log level changed to {logging.getLevelName(level)}")

    def set_debug_mode(self, enabled: bool = True) -> None:
        """
        Enable or disable DEBUG mode.

        Args:
            enabled: True - enable DEBUG, False - disable DEBUG
        """
        if enabled:
            self.set_log_level(logging.DEBUG)
            # Create debug handler if it wasn't created during initialization
            if not self._debug_handler and not self.config.debug:
                self._add_debug_handler()
        else:
            self.set_log_level(self.config.log_level)

    def _add_debug_handler(self) -> None:
        """Add a debug handler for DEBUG level logs if it doesn't exist."""
        log_dir = self.config.path_dir
        system_path = self.config.get_system_log_path()
        stem = system_path.stem
        suffix = system_path.suffix
        debug_path = log_dir / f"{stem}_debug{suffix}"

        self._debug_handler = RotatingFileHandler(
            filename=debug_path,
            maxBytes=self.config.max_bytes,
            backupCount=self.config.backup_count,
            encoding=self.config.encoding
        )
        self._debug_handler.setFormatter(logging.Formatter(self.config.system_format))
        self._debug_handler.setLevel(logging.DEBUG)
        logging.getLogger().addHandler(self._debug_handler)

        logging.getLogger(__name__).info("Debug logging enabled")

    def get_current_log_level(self) -> int:
        """Return the current effective log level of the root logger."""
        return logging.getLogger().getEffectiveLevel()

    def enable_logger_for_test(self, logger_name: str, level: int = logging.DEBUG) -> None:
        """
        Enable detailed logging for a specific logger (useful for tests).

        Args:
            logger_name: Logger name (e.g., 'app.service.repository')
            level: Log level to set
        """
        test_logger = logging.getLogger(logger_name)
        test_logger.setLevel(level)

        # Add a console handler for tests if not already present
        if not any(isinstance(h, logging.StreamHandler) and h.level <= level
                   for h in test_logger.handlers):
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(logging.Formatter(self.config.system_format))
            test_logger.addHandler(console_handler)

    def disable_logging_for_test(self) -> None:
        """Disable all logging (useful for clean test output)."""
        logging.disable(logging.CRITICAL)

    def enable_logging_for_test(self) -> None:
        """Re-enable logging after disable_logging_for_test()."""
        logging.disable(logging.NOTSET)

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get a logger instance by name.

        Args:
            name: Logger name (typically __name__)

        Returns:
            logging.Logger instance

        Raises:
            RuntimeError: If logger hasn't been initialized
        """
        if Logger._instance is None:
            raise RuntimeError("Logger is not initialized. Call Logger.init_logger(config) first.")
        return logging.getLogger(name)

    @classmethod
    def init_logger(cls, logger_config: LoggerConfig) -> 'Logger':
        """
        Initialize the singleton logger instance.

        Args:
            logger_config: Logger configuration object

        Returns:
            Logger singleton instance
        """
        if not cls._instance:
            cls._instance = cls(logger_config)
        return cls._instance