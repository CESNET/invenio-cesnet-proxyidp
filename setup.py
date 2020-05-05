# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# Perun ProxyIDP OpenIDC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""CESNET Perun ProxyIDP OpenIDC auth backend"""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'isort>=4.3.3',
    'pydocstyle>=1.0.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.0',
]

invenio_search_version = '1.0.0'
invenio_db_version = '1.0.1'

setup_requires = [
    'Babel>=1.3',
]

install_requires = [
    'Flask-BabelEx>=0.9.3',
    'invenio-openid-connect>=1.2.1',
    'arrow>=0.12.1',
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_cesnet_proxyidp', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-cesnet-proxyidp',
    version=version,
    description=__doc__,
    long_description=readme,
    keywords='invenio-cesnet-proxyidp Invenio',
    license='MIT',
    author='Miroslav Bauer',
    author_email='bauer@cesnet.cz',
    url='https://github.com/CESNET/invenio-cesnet-proxyidp',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': [
            'proxyidp = invenio_app.cli:cli',
        ],
        'invenio_base.apps': [
            'invenio_cesnet_proxyidp = invenio_cesnet_proxyidp:InvenioCesnetProxyIDP',
        ],
        'invenio_base.api_apps': [
            'invenio_cesnet_proxyidp = invenio_cesnet_proxyidp:InvenioCesnetProxyIDP',
        ],
        "flask.commands": [
            "proxyidp = invenio_cesnet_proxyidp.cli:proxyidp",
        ],
    },
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 3 - Planning',
    ],
)
