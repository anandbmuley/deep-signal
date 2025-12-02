"""Setup configuration for DeepSignal."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="deep-signal",
    version="0.1.0",
    author="DeepSignal Team",
    description="Autonomous Tri-Agent AI screener for forensic candidate analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "python-dateutil>=2.8.2",
        "requests>=2.31.0",
        "pydantic>=2.0.0",
        "typing-extensions>=4.7.0",
        "PyGithub>=2.1.1",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "nltk>=3.8.1",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "test": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
