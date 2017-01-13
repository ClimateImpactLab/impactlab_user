#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements_install = [
    'click>=6.0',
    'PyYAML>=3.10',
    'Sphinx>=1.4.1',
    'sphinx_rtd_theme>=0.1.0',
    'boto>=2.30.0',
    'boto3>=1.0',
    'datafs>=0.6.3',
    'jinja2>=2.8'
    ]

requirements_test = [
    'click>=6.0',
    'PyYAML>=3.10',
    'Sphinx>=1.4.1',
    'sphinx_rtd_theme>=0.1.0',
    'boto>=2.30.0',
    'boto3>=1.0',
    'datafs>=0.6.3',
    'jinja2>=2.8',
    'pip>=8.0',
    'wheel>=0.27',
    'flake8>=2.0',
    'tox>=2.3.0',
    'coverage>=4.0',
    'pytest>=3.0',
    'pytest_cov>=2.0',
    'pytest-runner>=2.5'
    ]

extras = {
    'test': requirements_test
}


entry_points = '[console_scripts]\nimpactlab-user=impactlab_user.cli:cli'

setup(
    name='impactlab_user',
    version='0.1.4',
    description="Set up users to use Climate Impact Lab tools",
    long_description=readme,
    author="Climate Impact Lab",
    url='https://github.com/ClimateImpactLab/impactlab_user',
    packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests', 'docs', 'examples']),
    package_dir={'impactlab_user':
                 'impactlab_user'},
    include_package_data=True,
    install_requires=requirements_install,
    entry_points=entry_points,
    license="MIT license",
    zip_safe=False,
    keywords='impactlab_user',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7'
    ],
    test_suite='tests',
    setup_requires=['pytest-runner'],
    tests_require=requirements_test,
    extras_require=extras
)
