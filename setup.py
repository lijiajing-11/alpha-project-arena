"""ARA - Arena Star Tracker."""
import os

from setuptools import setup, find_packages


HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ara",
    version="0.3.0",
    description="ARA - Arena Star Tracker: Monitor and compare GitHub Stars",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lijiajing-11/alpha-project-arena",
    author="A-Tech Inc.",
    author_email="dev@alpha-project.dev",
    license="MIT",
    install_requires=[
        "plyer>=2.1",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    packages=find_packages(exclude=["tests"]),
    entry_points={
        "console_scripts": [
            "ara=ara.cli:main",
        ],
    },
    project_urls={
        "Source": "https://github.com/lijiajing-11/alpha-project-arena",
        "Bug Reports": "https://github.com/lijiajing-11/alpha-project-arena/issues",
    },
)
