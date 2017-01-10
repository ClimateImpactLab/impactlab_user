#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements_install = [
    'click==6.6',
    'PyYAML==3.12',
    'Sphinx==1.5.1',
    'sphinx_rtd_theme==0.1.10a0',
    'boto==2.45.0',
    'boto3==1.4.3',
    'datafs==0.6.2',
    'jinja2==2.9.2'
]


requirements_test = [
    'pip==9.0.1',
    'wheel==0.29.0',
    'flake8==3.2.1',
    'tox==2.5.0',
    'coverage==4.3.1',
    'pytest==3.0.5',
    'pytest_cov==2.4.0',
    'pytest-runner==2.9'
]

extras = {
    'test': requirements_test
}


entry_points = '[console_scripts]\nimpactlab-user=impactlab_user.cli:cli'

setup(
    name='impactlab_user',
    version='0.0.1',
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
    tests_require=requirements_test,
    extras_require=extras
)
