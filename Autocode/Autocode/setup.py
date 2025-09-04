#!/usr/bin/env python3
"""
Setup script for datamodel_profiler package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="datamodel_profiler",
    version="1.0.0",
    author="Data Model Profiler Team",
    author_email="team@datamodelprofiler.com",
    description="A production-ready Python package for data profiling and schema inference",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/datamodel_profiler",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "html": ["ydata-profiling>=4.0.0"],
        "polars": ["polars>=0.20.0"],
        "orc": ["pyarrow>=10.0.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "datamodel-profiler=datamodel_profiler.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
