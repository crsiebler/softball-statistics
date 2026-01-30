from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="softball-statistics",
    version="0.1.0",
    author="Softball Statistics Team",
    author_email="team@softball-stats.com",
    description="A comprehensive softball statistics tracker for multiple leagues and teams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/crsiebler/softball-statistics",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Sports Enthusiasts",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.5.0",
        "openpyxl>=3.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov",
        ],
    },
    entry_points={
        "console_scripts": [
            "softball-stats = softball_statistics.cli:main",
        ],
    },
)
