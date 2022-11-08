#!/usr/bin/env python3

'''Ejemplo de API REST para ADI'''

from setuptools import setup

setup(
    name='restauth',
    version='0.1',
    description=__doc__,
    packages=['restauth', 'restauth_scripts'],
    entry_points={
        'console_scripts': [
            'restauth_server=restauth_scripts.server:main',
            'restauth_client=restauth_scripts.client:main'
        ]
    }
)