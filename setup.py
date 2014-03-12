#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Chronicler',
    'author': 'Alexander D Brown',
    'url': 'https://github.com/SoftlySplinter/chronicler',
    'download_url':'https://github.com/SoftlySplinter/chronicler/archive/master.zip',
    'author_email': 'alex@alexanderdbrown.com',
    'version': '0.1',
    'install_requires': ['flask'],
    'test_requires': ['nose'],
    'packages': ['chronicler'],
    'scripts': [],
    'entry_points': {
        'console_scripts': ['chronicler = chronicler:run']
    },
    'name': 'Chronicler'
}

setup(**config)
