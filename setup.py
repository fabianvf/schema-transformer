from setuptools import setup

VERSION = '0.0.3'

install_reqs = [
    'jsonpointer',
    'jsonschema',
    'six'
]

setup(
    name='schema-transformer',
    packages=['schema_transformer'],
    version=VERSION,
    description='A library for doing schema transformations',
    author='Fabian von Feilitzsch',
    author_email='fabian@cos.io',
    url='https://github.com/fabianvf/schema-transformer',
    download_url='https://github.com/fabianvf/schema-transformer/tarball/{}'.format(VERSION),
    install_requires=install_reqs
)
