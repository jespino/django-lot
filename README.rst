Django Login over Token
=======================

.. image:: https://travis-ci.org/jespino/django-lot.png?branch=master
    :target: https://travis-ci.org/jespino/django-lot

.. image:: https://coveralls.io/repos/jespino/django-lot/badge.png?branch=master
    :target: https://coveralls.io/r/jespino/django-lot?branch=master

.. image:: https://pypip.in/v/django-lot/badge.png
    :target: https://crate.io/packages/django-lot

.. image:: https://pypip.in/d/django-lot/badge.png
    :target: https://crate.io/packages/django-lot

Django Login over Token easy the creation of token based logins. Can be
one-time-logins, temporary valid logins or permanent logins, always based on
your settings.

How to install
--------------

You can also install it with: ``pip install django-lot``


Configuration
-------------

Add the lot app to your installed apps and define your settings :code:`LOT`
variable as a dictionary and :code:`LOT_MIDDLEWARE_PARAM_NAME` if you use the
lot middleware.

Example::

  LOT = {
    'fast-login': {
        'name': _(u'Fast login'),
        'duration': 60,
        'one-time': True,
    },
    'slow-login': {
        'name': _(u'Slow login'),
        'duration': 60*60*24,
        'one-time': True,
    },
    'always-login': {
        'name': _(u'Always login'),
        'one-time': False,
        'duration': None,
    },
    'morning-login': {
        'name': _(u'Morning login'),
        'one-time': False,
        'duration': None,
        'verify-func': lambda x: datetime.now().hour < 12,
        'delete-on-fail': False
    },
  }

  LOT_MIDDLEWARE_PARAM_NAME = 'uuid-login'

GET key
-------

Add the lot authentication backend to the :code:`AUTHENTICATION_BACKENDS`
settings variable.

Example::

  AUTHENTICATION_BACKENDS = (
      "django.contrib.auth.backends.ModelBackend",
      "lot.auth_backend.LOTBackend",
  )


Header Key
----------

Add the lot authentication middleware to the :code:`MIDDLEWARE_CLASSES`
settings variable.  Ensure it is __after__ Django's AuthenticationMiddleware.

Example::

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'lot.middleware.LOTAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    )

warning::

   This method should ONLY be used over HTTPS.

Usage
-----

You have to create the LOT instances with a user and a type (the uuid and the
created date are auto-generated). Then you can use the lot login view, or the
the lot login middleware. You can set the session_data attribute to add data
to the user session when login with LOT.

If you use the lot middleware you can login in any url that have the param
defined in the :code:`LOT_MIDDLEWARE_PARAM_NAME` and have a valid LOT instance
related to it.

If you use the view you can add the next param to redirect the user to an url
after the login. By default will redirect you to the "/" url.
