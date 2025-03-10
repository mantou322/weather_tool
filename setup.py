from setuptools import setup, find_packages
from src import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="weather_tool",
    version=__version__,
    author="Author",
    author_email="author@example.com",
    description="A weather tool application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/weather_tool",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "python-dotenv>=0.19.0",
        "requests>=2.26.0",
    ],
)