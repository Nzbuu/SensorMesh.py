#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'requests',
    'python-dateutil',
    'tweepy'
]
test_requirements = [
    'pytest',
    'pytest-cov',
    'responses',
    'textfixtures'
]
setup_requirements = [
    'bumpversion',
    'pytest-runner'
]

setup(
    name="SensorMesh",
    version="0.0.3.dev1",
    description="",
    long_description=readme,
    author="James Myatt",
    author_email='james@jamesmyatt.co.uk',
    url='https://github.com/Nzbuu/SensorMesh.py',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements
)
