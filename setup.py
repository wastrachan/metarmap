from setuptools import find_packages, setup

setup(
    name='metarmap',
    version='0.0.1',
    author='Winston Astrachan',
    description='Metar Map',
    url='https://github.com/wastrachan/metarmap',
    packages=find_packages(),
    install_requires=[
        'certifi==2021.5.30',
        'charset-normalizer==2.0.4',
        'click==8.0.1',
        'docutils==0.17.1',
        'idna==3.2',
        'lockfile==0.12.2',
        'lxml==4.6.3',
        'python-daemon==2.3.0',
        'requests==2.26.0',
        'rpi-ws281x==4.3.0',
        'urllib3==1.26.6',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Home Automation',
        'Topic :: Utilities',
        'Topic :: System :: Hardware',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'metarmap=metarmap.main:cli',
        ],
    },
)
