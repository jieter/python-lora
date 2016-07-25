#!/usr/bin/env python

import os
import sys

from setuptools import setup

from lora import VERSION

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    os.system("git tag -a v{} -m 'tagging v{}'".format(VERSION, VERSION))
    os.system('git push && git push --tags')
    sys.exit()


setup(
    name='python-lora',
    version=VERSION,
    description='Decrypt LoRa payloads',
    url='https://github.com/jieter/python-lora',

    author='Jan Pieter Waagmeester',
    author_email='jieter@jieter.nl',
    license='MIT',

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='LoRa decrypt',
    packages=['lora'],

    install_requires=[
        'cryptography==1.4'
    ],
)
