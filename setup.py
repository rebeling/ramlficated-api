# -*- coding: utf-8 -*-
from setuptools import setup
import yaml

config = yaml.load(open('etc/conf.yml', 'r').read())


setup(
    name=config['name'],
    version=config['version'],
    author=config['author'],
    author_email=config.get('author_email'),
    url=config.get('url'),
    description=open('readme.md', 'rt').read(),
    packages=[config['name']],
    install_requires=[
        line.split('==')[0]
        for line in open('requirements.txt', 'rt').read().split('\n')
    ]
)
