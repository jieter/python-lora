from setuptools import setup

from lora import VERSION

setup(
    name='python-lora',
    version=VERSION,
    description='Decrypt LoRa payloads',
    url='https://github.com/jieter/python-lora',

    author='Jan Pieter Waagmeester',
    author_email='jieter@jieter.nl',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='LoRa decrypt',
    packages=['lora'],

    install_requires=[
        'lxml==3.5.0',
        'pycrypto==2.6.1'
    ],
)
