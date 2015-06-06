from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='NodeFinder',
    version='0.1.2',
    description='Tools for node related operations in phylogenetic analyses.',
    author='Haofei Jin',
    author_email='zxjsdp@gmail.com',
    url='https://github.com/zxjsdp',
    license='Apache',
    keywords='node phylogenetic tools calibration',
    packages=['nodefinder'],
    install_requires=[],
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
