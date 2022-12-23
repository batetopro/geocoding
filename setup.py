#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "geocoder",
    "requests",
]

test_requirements = [ ]

setup(
    author="Hrsito Georgiev",
    author_email='hristo.i.georgiev@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Take a list of pairs of name and address. Then group people living on the same address.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='geocoding',
    name='geocoding',
    packages=find_packages(include=['geocoding', 'geocoding.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/batetopro/geocoding',
    version='0.1.0',
    zip_safe=False,
)
