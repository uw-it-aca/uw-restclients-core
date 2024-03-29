# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/uw-restclients-core>`_.
"""

version_path = 'restclients_core/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

url = "https://github.com/uw-it-aca/uw-restclients-core"
setup(
    name='UW-RestClients-Core',
    version=VERSION,
    packages=['restclients_core'],
    author="UW-IT T&LS",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=['commonconf',
                      'urllib3',
                      'python-dateutil',
                      'prometheus-client',
                      'mock'],
    license='Apache License, Version 2.0',
    description=('Core code for clients of a variety of RESTful web services '
                 'at the University of Washington'),
    long_description=README,
    url=url,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
