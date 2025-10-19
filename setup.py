"""
Setup script for btc-indicators package.
This file provides backwards compatibility with older pip versions.
Modern installations should use pyproject.toml.
"""

from setuptools import setup, find_packages

setup(
    name="btc-indicators",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        "yfinance>=0.2.0",
        "pandas>=1.3.0",
        "matplotlib>=3.3.0",
        "numpy>=1.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
        ],
    },
    python_requires=">=3.8",
)

