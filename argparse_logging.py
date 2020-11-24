import logging
from argparse import Action, ArgumentParser, Namespace
from typing import Any, Optional, Sequence, Union
from enum import Enum


class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    FATAL = logging.FATAL

    def __str__(self):
        return self.name


class LoggingAction(Action):
    """Abstraction for the different log parsers."""

    def __init__(self: "LoggingAction", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        logging.basicConfig()
        self.configure(self.default)

    def __call__(
        self: "LoggingAction",
        parser: ArgumentParser,
        namespace: Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = None,
    ) -> None:
        self.configure(values)
        setattr(namespace, self.dest, values)

    def configure(self: "LoggingAction", level: Any) -> None:
        raise NotImplementedError


class LogLevelAction(LoggingAction):
    """Simple argparse action to manage logging level."""

    def configure(self: "LogLevelAction", level: int) -> None:
        assert isinstance(level, LogLevel)
        logging.getLogger().setLevel(level.value)


def add_log_level_argument(
    parser: ArgumentParser, option_string: str = "--log-level"
) -> Action:
    """Add argument and action to configure the log level."""
    return parser.add_argument(
        option_string,
        choices=list(LogLevel),
        type=lambda x: getattr(LogLevel, x),
        default=LogLevel.INFO,
        action=LogLevelAction,
        help="Logging level.",
    )


class LogFormatAction(LoggingAction):
    """Configure the logging format."""

    def configure(self: "LogFormatAction", fmt: str) -> None:
        formatter = logging.Formatter(fmt)
        for handler in logging.getLogger().handlers:
            handler.setFormatter(formatter)


def add_log_format_argument(
    parser: ArgumentParser, option_string: str = "--log-format"
) -> Action:
    """Add argument and action to configure the log format."""
    return parser.add_argument(
        option_string,
        default="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
        action=LogFormatAction,
        help="Logging format."
        "See https://docs.python.org/3/library/logging.html#logrecord-attributes",
    )


def add_logging_arguments(parser):
    add_log_format_argument(parser)
    add_log_level_argument(parser)
