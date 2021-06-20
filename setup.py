# -*- coding: utf-8 -*-
import os

from setuptools import setup

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'

description = """
Django Login over Token.
"""

setup(
    name = "django-lot",
    url = "https://github.com/jespino/django-lot",
    author = "Jesús Espino, Curtis Malone",
    author_email = "jespinog@gmail.com, curtis@tinbrain.net",
    version='v0.2.2-uptick',
    packages = [
        "lot",
        "lot.migrations",
    ],
    description = description.strip(),
    install_requires=['django >= 3.0', 'simplejson >= 3.3.0'],
    setup_requires = [
        'versiontools >= 1.8',
    ],
    zip_safe=False,
    include_package_data = False,
    package_data = {},
    test_suite = 'nose.collector',
    tests_require = ['nose >= 1.2.1', 'django >= 3.0'],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.0",
    ],
)
