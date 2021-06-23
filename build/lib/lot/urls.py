# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^login/(?P<uuid>[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12})/$", views.LOTLogin.as_view(), name="login"),
]
