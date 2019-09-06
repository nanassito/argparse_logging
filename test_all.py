import logging
import re
from argparse import ArgumentParser
from tempfile import NamedTemporaryFile

import pytest

from argparse_logging import add_logging_arguments


@pytest.mark.parametrize(
    ["args", "logs_rx"],
    [
        (  # Using defaults
            [],
            [
                r"\d{4}(\-\d{2}){2}\s\d{2}(:\d{2}){2},\d{3}:INFO:root:My log line",
                r"\d{4}(\-\d{2}){2}\s\d{2}(:\d{2}){2},\d{3}:INFO:child:My log line",
                r"\d{4}(\-\d{2}){2}\s\d{2}(:\d{2}){2},\d{3}:WARNING:root:My log line",
                r"\d{4}(\-\d{2}){2}\s\d{2}(:\d{2}){2},\d{3}:WARNING:child:My log line",
                r"\d{4}(\-\d{2}){2}\s\d{2}(:\d{2}){2},\d{3}:ERROR:root:My log line",
                r"\d{4}(\-\d{2}){2}\s\d{2}(:\d{2}){2},\d{3}:ERROR:child:My log line",
            ],
        ),
        (  # Decreasing the level
            ["--log-level=DEBUG"],
            [
                r"\d{4}(\-\d{2}){2}\s\d{2}(:\d{2}){2},\d{3}:DEBUG:root:My log line",
                r"\d{4}(\-\d{2}){2}\s\d{2}(:\d{2}){2},\d{3}:DEBUG:child:My log line",
                r"\d{4}(\-\d{2}){2}\s\d{2}(:\d{2}){2},\d{3}:INFO:root:My log line",
                r"\d{4}(\-\d{2}){2}\s\d{2}(:\d{2}){2},\d{3}:INFO:child:My log line",
                r"\d{4}(\-\d{2}){2}\s\d{2}(:\d{2}){2},\d{3}:WARNING:root:My log line",
                r"\d{4}(\-\d{2}){2}\s\d{2}(:\d{2}){2},\d{3}:WARNING:child:My log line",
                r"\d{4}(\-\d{2}){2}\s\d{2}(:\d{2}){2},\d{3}:ERROR:root:My log line",
                r"\d{4}(\-\d{2}){2}\s\d{2}(:\d{2}){2},\d{3}:ERROR:child:My log line",
            ],
        ),
        (  # Increasing the level
            ["--log-level=ERROR"],
            [
                r"\d{4}(\-\d{2}){2}\s\d{2}(:\d{2}){2},\d{3}:ERROR:root:My log line",
                r"\d{4}(\-\d{2}){2}\s\d{2}(:\d{2}){2},\d{3}:ERROR:child:My log line",
            ],
        ),
        (  # Using a custom format
            ["--log-format=HEADER>%(message)s<FOOTER"],
            [
                r"HEADER>My log line<FOOTER",  # root info
                r"HEADER>My log line<FOOTER",  # child info
                r"HEADER>My log line<FOOTER",  # root warning
                r"HEADER>My log line<FOOTER",  # child warning
                r"HEADER>My log line<FOOTER",  # root error
                r"HEADER>My log line<FOOTER",  # child error
            ],
        ),
        (  # Using a custom format and custom level
            ["--log-level=WARNING", "--log-format=%(name)s~%(levelname)s~%(message)s"],
            [
                r"root~WARNING~My log line",
                r"child~WARNING~My log line",
                r"root~ERROR~My log line",
                r"child~ERROR~My log line",
            ],
        ),
    ],
)
def test_end_to_end(args, logs_rx):
    with NamedTemporaryFile() as log_file:
        handler = logging.FileHandler(log_file.name)
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        child_logger = logging.getLogger("child")

        parser = ArgumentParser()
        parser.add_argument("foo")
        add_logging_arguments(parser)

        namespace = parser.parse_args(["bar"] + args)
        for level in ("debug", "info", "warning", "error"):
            getattr(root_logger, level)("My log line")
            getattr(child_logger, level)("My log line")
        handler.close()  # Needed to make sure the logs hit the disk

        with open(log_file.name) as fd:
            lines = fd.readlines()

    assert namespace.foo == "bar", "Lost a user supplied argument"
    assert len(lines) == len(logs_rx)
    for line, log_rx in zip(lines, logs_rx):
        assert re.match(log_rx, line) is not None, f"'{line}' doesn't match /{log_rx}/"
