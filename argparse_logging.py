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


class LogLevelParser(Action):
    """Simple argparse action to manage logging level."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        logging.getLogger().setLevel(self.default)

    def __call__(
        self: "LogLevelParser",
        parser: ArgumentParser,
        namespace: Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = None,
    ) -> None:
        assert isinstance(values, LogLevel)
        logging.getLogger().setLevel(values.value)
        setattr(namespace, self.dest, values.value)


def add_log_level_argument(
    parser: ArgumentParser, option_string: str = "--log-level"
) -> Action:
    """Add argument and action to configure the log level."""
    return parser.add_argument(
        option_string,
        choices=list(LogLevel),
        type=lambda x: getattr(LogLevel, x),
        default=LogLevel.INFO.value,
        action=LogLevelParser,
        help=f"Logging level ({[l.name for l in LogLevel]}).",
    )
