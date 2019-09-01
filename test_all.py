import logging
from argparse import ArgumentParser, Namespace

import pytest

from argparse_logging import add_log_level_argument


@pytest.mark.parametrize(
    ["logging_args", "expected_level"],
    [
        # Test using the default
        ([], logging.INFO),
        # Test using use input
        (["--log-level", "DEBUG"], logging.DEBUG),
    ],
)
def test_using_defaults(logging_args, expected_level):
    parser = ArgumentParser()
    # Make sure the other arguments aren't impacted
    parser.add_argument("foo")
    parser.add_argument("--bar", default="something")
    loggers = [logging.getLogger(), logging.getLogger(__name__)]

    add_log_level_argument(parser)
    args = parser.parse_args(["foo_val", "--bar", "bar_val"] + logging_args)

    assert args == Namespace(log_level=expected_level, foo="foo_val", bar="bar_val")
    for logger in loggers:
        # Make sure all loggers are configured.
        assert logger.getEffectiveLevel() == expected_level
