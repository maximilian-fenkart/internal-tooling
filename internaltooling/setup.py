"""Installable internal tooling package."""

from setuptools import find_packages, setup

setup(
    name="internaltooling",
    version="0.1.0",
    description="Internal tooling",
    python_requires=">=3.12",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    package_data={
        "internaltooling": ["source-data/*"],
    },
    install_requires=[
        "pillow>=11",
        "qrcode>=8",
        "reportlab>=4",
        "svglib>=1.5",
    ],
    extras_require={
        "dev": ["pytest>=8"],
    },
    entry_points={
        "console_scripts": [
            "generate-serial-stickers=internaltooling.serial_numbers.cli:main",
        ],
    },
)
