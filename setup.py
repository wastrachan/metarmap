from setuptools import find_packages, setup

setup(
    name="metarmap",
    version="0.4.0",
    author="Winston Astrachan",
    description="Metar Map",
    url="https://github.com/wastrachan/metarmap",
    packages=find_packages(),
    install_requires=[
        "certifi==2024.7.4",
        "charset-normalizer==3.3.2",
        "click==8.1.7",
        "colorzero==2.0",
        "gpiozero==2.0.1",
        "idna==3.7",
        "lgpio==0.2.2.0",
        "lxml==5.2.2",
        "numpy==2.0.1",
        "pillow==10.4.0",
        "requests==2.32.3",
        "RPi.GPIO==0.7.1",
        "rpi_ws281x==5.0.0",
        "spidev==3.6",
        "urllib3==2.2.2",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Home Automation",
        "Topic :: Utilities",
        "Topic :: System :: Hardware",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "metarmap=metarmap.main:cli",
        ],
    },
)
