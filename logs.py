import sys
import logging
import os
from typing import Optional, Union, Final


class Logs:
    # Holds valid logging levels
    CONST_LOG_LEVELS: Final[set[int]] = {
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.CRITICAL,
        logging.ERROR,
        logging.NOTSET,
    }
    # Default formatter for logs
    DEFAULT_LOG_FORMATTER: Final[logging.Formatter] = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    def __init__(
        self,
        name: Union[str, None] = None,
        level: int = logging.INFO,
        log_file: Union[str, None] = None,
    ):
        """
        Initializes the logging class.

        :param name: Optional. Loggers name. Defaults to module's __name__
        :type name: Union[str,None]

        :param level: Optional. Minimum log level to capture. Defaults to logging.INFO
        :type level: int

        :param log_file: Optional. Path for writing files. If None, file outputs to console.
        :type log_file: Union[str,None]
        :raise TypeError: If level is not type(int)
        :raise ValueError: If level is not in CONST_LOG_LEVELS

        """
        # Run initial checks to ensure valid level
        if not isinstance(level, int):
            raise TypeError("Incorrect Type for level value,must be type(int)")
        if level not in self.CONST_LOG_LEVELS:
            raise ValueError(f"Invalid level,level must be:{self._get_level_names()}")
        self._logger: logging.Logger = self._configure_logger(
            name
        )  # list of active handlers for logs
        self._active_handlers: list[logging.Handler] = []
        self._log_path_value = None  # Holds path for logs
        self._formatter: logging.Formatter = self.DEFAULT_LOG_FORMATTER
        # Log path and handler setup
        self._log_path_value = log_file
        try:
            if log_file is None:
                # method to set handlers
                self._config_console_handlers()
            else:
                self._set_file_handler(log_file)
        except (IOError, OSError) as e:
            # If file setup fails fall back to console
            self._log_path_value = None
            self._set_stream_handler()
            print(f"Failed to set log path to:{log_file}.Defaulting to console:{e}")
        # Apply logic for instance variables via setters
        self.log_level = level
        self.log_path = log_file  # Optional path for logs,defaults to console

    def __str__(self):
        """
        String representation of Logs object
        """
        # Get level name
        level_name = logging.getLevelName(self.log_level)
        # Determines path: str or console if None
        path_str = self.log_path if self.log_path is not None else "console"
        return (
            f"Logs(name='{self.log_name}'," f"level={level_name}," f"path='{path_str}')"
        )

    def _configure_logger(self, name: Union[str, None]) -> logging.Logger:
        """
        Configures name for loggers:
        Logs with the same name are reused

        :param name: Holds name for logger,defaults to None if not set
        :type name: Union[str,None]
        :return: logging.Logger instance
        """
        logger_name = (
            name if name else __name__
        )  # If name is avaible use name,else use module name
        logger = logging.getLogger(logger_name)
        logger.propagate = False  # Prevent duplicate logs from root logger
        # Reset logger level
        logger.setLevel(logging.NOTSET)
        # Removing existing handlers
        if logger.hasHandlers():
            logger.handlers.clear()
        return logger

    @property
    def log_name(self) -> str:
        """
        Holds the name of current logger instance
        :return: logger name
        :rtype: str
        """
        return self._logger.name

    @property
    def log_level(self) -> int:
        """
        Obtains current logging level for logger
        :return current log level as int
        :rtype: int
        """
        return self._logger.level

    @log_level.setter
    def log_level(self, level_value: int):
        """
        Sets the logging level for logger instance and active handler.
        :param level_value: Logger level
        :type level_value: int
        :raise TypeError: if type(level_value) is not type(int)
        :raise ValueError: if level_value is not one of the following:[DEBUG,WARNING,INFO,NOTSET,ERROR,CRITICAL]

        """
        if not isinstance(level_value, int):
            raise TypeError(
                f"Incorrect datatype input for level_value: expects type(int),received type:{type(level_value)}"
            )

        # Check if a valid logging.LEVEL was set
        if level_value not in self.CONST_LOG_LEVELS:
            raise ValueError(
                f"Incorrect value for logging level. Valid levels:{self._get_level_names()}"
            )

        if self._logger:
            self._logger.setLevel(level_value)
            # Update active handler's level
            for handler in self._active_handlers:
                handler.setLevel(level_value)

    @property
    def log_path(self) -> Optional[str]:
        """
        Retrieves current log path.Path defaults to None if not set
        :return: file path as a str or None if logging to console.
        :rtype:Optional[str]
        """
        return self._log_path_value  # Holds current path

    @log_path.setter
    def log_path(self, new_path_value: Union[str, None]):
        """
        Handles file path for logs.
        Logs to console by default if None.
        Removes old handlers and adds new handlers

        :param new_path_value: Holds value for possible logger path
        :type new_path_value: Union[str,None]
        :raise TypeError: If new_path_value is not type(str)
        """
        # Check for correct path value
        if new_path_value is not None and not isinstance(new_path_value, str):
            raise TypeError("Log's path must be string or None")

        if self._log_path_value == new_path_value:
            return
        # Store path for logs
        self._log_path_value = new_path_value
        if not self._logger:
            print("No _logger instance found")
            return
        # Remove any existing handlers for logs
        self._remove_all_handlers()
        try:
            # Generate new handler based on path balue
            if new_path_value is None:
                # Split console output
                self.setup_console_handlers()
            else:
                self._set_file_handler(new_path_value)
        except IOError as e:
            # In case of file system errors,default to stream handler
            self._setup_console_handlers()  # Defaults to console
            raise IOError(
                f"Could not set log path to: {new_path_value} error {e}"
            ) from e

    def _remove_all_handlers(self):
        """Removes and closes all current handlers if one exists"""
        for handler in self._active_handlers:
            if handler in self._logger.handlers:  # Check for existing handler
                self._logger.removeHandler(handler)
            handler.close()
            self._active_handlers.clear()

    def _config_console_handlers(self):
        """
        Sets stream handlers for console output.
        DEBUG,INFO,WARNING output: sys.stdout.
        CRITICAL,ERROR output: sys.stderr.
        """
        # If called dynamically, previous handler is removed
        self._remove_all_handlers()

        # Handler for sys.stdout:(WARNING,INFO,DEBUG)
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(self._formatter)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.addFilter(lambda record: record.levelno <= logging.WARNING)
        # Handler for sys.stderr:(CRITICAL,ERROR)
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setFormatter(self._formatter)
        stderr_handler.setLevel(logging.ERROR)

        self._logger.addHandler(stderr_handler)
        self._logger.addHandler(stdout_handler)
        self._active_handlers.extend([stdout_handler, stderr_handler])

        self._logger.setLevel(logging.DEBUG)

    def _set_stream_handler(self):
        """Configures and sets stream handler"""
        if logging.StreamHandler is logging.INFO or logging.DEBUG or logging.WARNING:
            new_handler = logging.StreamHandler(sys.stdout)
            new_handler.setFormatter(self._formatter)
        else:
            new_handler = logging.StreamHandler(sys.stderr)
        new_handler.setFormatter(self._formatter)
        # set handler level to reflect logger level
        new_handler.setLevel(self._logger.level)
        self._logger.addHandler(new_handler)
        self._current_handler = new_handler

    def _set_file_handler(self, file_path: str):
        """
        Configures and sets a file handler,if necessary,creates directories
        :param file_path: stores path for handler
        :raise IOError: If file or directory cannot be created
        """
        logger_dir = os.path.dirname(file_path)
        if logger_dir and not os.path.exists(logger_dir):
            os.makedirs(logger_dir, exist_ok=True)
        new_handler = logging.FileHandler(file_path)  # updates new_handler to file_path
        new_handler.setFormatter(self._formatter)
        # Sets Handler's level to match logger's level
        new_handler.setLevel(self._logger.level)
        self._logger.addHandler(new_handler)
        self._active_handlers.append(new_handler)  # Add to list of _active_handlers

    def _get_level_names(self) -> str:
        """Helper function:Gets the logger level."""
        return ", ".join(logging.getLevelName(level) for level in self.CONST_LOG_LEVELS)

    # Methods for logging
    def debug(self, message: str, *args, **kwargs):
        """
        Handles logs for Debugging severity level
        :param message: Holds message for debugging
        type message: str
        """
        self._logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """
        Handles logs for Info severity level
        :param message: Holds message for info
        :type message: str
        :raise TypeError: If message is not type(str)
        """
        self._logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """
        Handles logs for Warning severity level
        :param message: Holds warning message
        :type message: str
        :raise TypeError: If message is not type(str)
        """
        self._logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        """
        Handles logs for Error severity level
        :param message: Holds message for errors logs
        :type message: str
        :raise TypeError: If message is not type(str)
        """
        self._logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        """
        Handles logs for Critical severity level
        :param message: Holds message for critical logs
        :type message: str
        :raise TypeError: If message is not type(str)
        """
        self._logger.critical(message, *args, **kwargs)

    def close(self):
        """
        Releases memory used by logger.
        Removes and closes active handler
        """
        self._remove_all_handlers()


# Example usage


def example_console_logging():
    my_app_logs = Logs()
    print("_" * 35)
    print(f"Logger state:{my_app_logs}")
    my_app_logs.info("Application started successfully")
    my_app_logs.warning("A non-critical issue was detected")
    my_app_logs.error("An error occurred during a process")
    my_app_logs.critical("This is a critical test message")
    my_app_logs.debug("This message will not be shown as the level is INFO")
    my_app_logs.close()
    print("_" * 35)


example_console_logging()
