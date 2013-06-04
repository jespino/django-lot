.. image:: logo/logo.png

------

.. image:: https://travis-ci.org/jespino/django-fart.png?branch=master
    :target: https://travis-ci.org/jespino/django-fart

.. image:: https://coveralls.io/repos/jespino/django-fart/badge.png?branch=master
    :target: https://coveralls.io/r/jespino/django-fart?branch=master

.. image:: https://pypip.in/v/django-fart/badge.png
    :target: https://crate.io/packages/django-fart

.. image:: https://pypip.in/d/django-fart/badge.png
    :target: https://crate.io/packages/django-fart

Django Fast Authentication Request over Token easy the creation of token based
logins. Can be on-time-logins, temporary valid logins or permanent logins,
alwais based on your settings.

How to install
--------------

You can also install it with: ``pip install django-fart``


Configuration
-------------

Add the fart authentication backend to the :code:`AUTHENTICATION_BACKENDS`
settings variable.

Example::
  AUTHENTICATION_BACKENDS = (
      "django.contrib.auth.backends.ModelBackend",
      "fart.auth_backend.FARTBackend",
  )

Add the fart app to your installed apps and define your settings :code:`FART`
variable as a dictionary and :code:`FART_MIDDLEWARE_PARAM_NAME` if you use the
fart middleware.

Example::

  FART = {
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
    'alwais-login': {
        'name': _(u'Alwais login'),
        'one-time': False,
        'duration': None,
    },
  }

  FART_MIDDLEWARE_PARAM_NAME = 'uuid-login'

Usage
-----

You have to create the FART instances with a user and a type (the uuid and the
created date are auto-generated). Then you can use the fart login view, or the
the fart login middleware.

If you use the fart middleware you can login in any url that have the param
defined in the :code:`FART_MIDDLEWARE_PARAM_NAME` and have a valid FART instance
related to it.

If you use the view you can add the next param to redirect the user to an url
after the login. By default will redirect you to the "/" url.
