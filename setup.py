from setuptools import setup, find_packages

setup(
    name="ara",
    version="0.1.0",
    description="Arena Star Tracker — track and compare GitHub Stars from your terminal",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Alpha Corp",
    author_email="",
    url="https://github.com/li1050109098/alpha-project",
    packages=find_packages(),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "ara=ara.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Version Control",
        "Topic :: Utilities",
    ],
    license="MIT",
    keywords="github stars tracker cli arena battle",
)
