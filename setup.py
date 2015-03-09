#!/usr/bin/env python

from setuptools import setup

entry_points = {
    'console_scripts': [
        'radric = radric:main',
    ]
}

requirements = open('requirements.txt').read()
changelog = open('CHANGELOG.rst').read()
readme = open('README.rst').read()

setup(
    name="radric",
    version="0.1",
    url='http://github.com/ncrocfer/radric',
    author='Nicolas Crocfer',
    author_email='ncrocfer@gmail.com',
    description="A static website generator powered by Python",
    long_description=readme + "\n\n" + changelog,
    packages=['radric'],
    include_package_data=True,
    install_requires=requirements,
    entry_points=entry_points,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ),
)
