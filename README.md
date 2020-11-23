# Argparse_logging

This is a simple library to configure logging from command line argument when using argparse.

Without `argparse_logging`:
```
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument(
    "--log-level",
    default=logging.INFO,
    type=lambda x: getattr(logging, x)),
    help="Configure the logging level.",
)
args = parser.parse_args()
logging.basicConfig(level=args.log_level)
```

This is a bit annoying to copy paste in every program.

Instead you can use argparse_logging to get the following:
```
from argparse import ArgumentParser
from argparse_logging import add_log_level_argument

parser = ArgumentParser()
add_log_level_argument(parser)
args = parser.parse_args()
```

# Deployment

You will need `git`, `pipenv`, `python`, `pre-commit`. Then you can set up your virtual environment:

```
$ git clone git@github.com:nanassito/argparse_logging.git
$ cd argparse_logging
$ pipenv update --dev
```

Do whatever changes you want. You can run the tests and linting with:

```
$ pipenv run py.test
$ pre-commit
```
