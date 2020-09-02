#!/usr/bin/env python3

from setuptools import find_packages, setup

install_requires = [
    'pykeybasebot',
]

setup(
    name='keybase-piazza-bot',
    version='0.1.0.dev0',
    description='',
    url='https://github.com/andrew-fuchs/keybase-piazza-bot#readme',
    author='Andrew Fuchs',
    classifers=[
        'Framework :: AsyncIO',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: Communications :: Chat',
        'Topic :: Education',
    ],
    project_urls={
        'Source': 'https://github.com/andrew-fuchs/keybase-piazza-bot',
        'Tracker': 'https://github.com/andrew-fuchs/keybase-piazza-bot/issues',
    },

    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=install_requires,

    entry_points={
        'console_scripts': [
            'keybase-piazza-bot = keybase_piazza_bot:main',
        ],
    },
)
