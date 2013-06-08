# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

from fart.tests import TestView


urlpatterns = patterns("",
    url(r"", include('fart.urls')),
    url(r"^test_url/$", TestView.as_view()),
)
