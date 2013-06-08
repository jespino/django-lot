# -*- coding: utf-8 -*-
from setuptools import setup
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'

description = """
Django Fast Authenticate Request over Token.
"""

setup(
    name = "django-fart",
    url = "https://github.com/jespino/django-fart",
    author = "Jesús Espino",
    author_email = "jespinog@gmail.com",
    version=':versiontools:fart:',
    packages = [
        "fart",
    ],
    description = description.strip(),
    install_requires=['django >= 1.3.0', 'simplejson >= 3.3.0'],
    setup_requires = [
        'versiontools >= 1.8',
    ],
    zip_safe=False,
    include_package_data = False,
    package_data = {},
    test_suite = 'nose.collector',
    tests_require = ['nose >= 1.2.1', 'django >= 1.3.0'],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
)
