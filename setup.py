from setuptools import setup

VERSION = '0.0.0'

install_reqs = []
setup(
    name='schema_transformer',
    packages=['schema_transformer'],
    version=VERSION,
    description='',
    author='Fabian von Feilitzsch',
    author_email='fabian@cos.io',
    url='https://github.com/fabianvf/schema-transformer',
    download_url='https://github.com/fabianvf/schema-transformer/tarball/{}'.format(VERSION),
    install_requires=install_reqs
)