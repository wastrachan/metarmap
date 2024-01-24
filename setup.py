from setuptools import find_packages, setup

setup(
    name="metarmap",
    version="0.4.0",
    author="Winston Astrachan",
    description="Metar Map",
    url="https://github.com/wastrachan/metarmap",
    packages=find_packages(),
    install_requires=[
        "certifi==2023.11.17",
        "charset-normalizer==3.3.2",
        "click==8.1.7",
        "idna==3.6",
        "lxml==5.1.0",
        "numpy==1.26.3",
        "pillow==10.2.0",
        "requests==2.31.0",
        "rpi-ws281x==5.0.0",
        "urllib3==2.1.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
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
