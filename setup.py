from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="argparse_logging",
    version="0.3",
    author="Dorian Jaminais",
    author_email="argparse_logging@jaminais.fr",
    description="This is a simple library to configure logging from command "
    "line argument when using argparse.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nanassito/argparse_logging",
    py_modules=["argparse_logging"],
    test_suite="test_all",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
