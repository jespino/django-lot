import simplejson
import datetime

from django.utils import unittest
from django.conf import settings
from django.template import Template, Context
from django.core.management import call_command
from django.test.client import Client
from django.views.generic import View
from django.http import HttpResponse

from django.contrib.auth import get_user_model

from fart.models import FART

call_command('syncdb', interactive=False)

class TestView(View):
    def get(self, request):
        return HttpResponse()


class TestFARTBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        get_user_model().objects.all().delete()
        FART.objects.all().delete()

        test_user = get_user_model().objects.create(username="test")
        cls.fart1 =FART.objects.create(
                user=test_user,
                type="fast-login",
        )
        cls.fart2 =FART.objects.create(
                user=test_user,
                type="slow-login",
        )
        cls.fart3 =FART.objects.create(
                user=test_user,
                type="always-login",
        )
        cls.fart4 =FART.objects.create(
                user=test_user,
                type="always-login",
                session_data=simplejson.dumps({'data':'test'}),
        )


class TestFARTView(TestFARTBase):
    def test_fart_login_view_not_valid(self):
        c = Client()
        false_uuid = '12341234-1234-1234-1234-123412341234'
        response = c.get('/login/{0}/'.format(false_uuid))
        self.assertEqual(response.status_code, 404)

    def test_fart_login_view_one_time(self):
        c = Client()
        farts = FART.objects.all().count()
        response = c.get('/login/{0}/'.format(self.fart1.uuid))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(c.session['_auth_user_id'], 1)

        self.assertEqual(FART.objects.all().count(), farts-1)

        response = c.get('/login/{0}/'.format(self.fart1.uuid))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(c.session['_auth_user_id'], 1)

        self.assertEqual(FART.objects.all().count(), farts-1)

    def test_fart_login_view_temporary_valid(self):
        c = Client()
        farts = FART.objects.all().count()
        response = c.get('/login/{0}/'.format(self.fart2.uuid))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(c.session['_auth_user_id'], 1)

        self.assertEqual(FART.objects.all().count(), farts)

        c.logout()
        self.assertFalse("_auth_user_id" in c.session)

        self.fart2.created = self.fart2.created - datetime.timedelta(days=10)
        self.fart2.save(force_modification=True)

        response = c.get('/login/{0}/'.format(self.fart2.uuid))
        self.assertEqual(response.status_code, 404)
        self.assertFalse("_auth_user_id" in c.session)

        self.assertEqual(FART.objects.all().count(), farts-1)

    def test_fart_login_view_allways_valid(self):
        c = Client()
        farts = FART.objects.all().count()

        response = c.get('/login/{0}/'.format(self.fart3.uuid))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(c.session['_auth_user_id'], 1)

        c.logout()
        self.assertFalse("_auth_user_id" in c.session)

        self.assertEqual(FART.objects.all().count(), farts)

        response = c.get('/login/{0}/'.format(self.fart3.uuid))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(c.session['_auth_user_id'], 1)

        c.logout()
        self.assertFalse("_auth_user_id" in c.session)

        self.assertEqual(FART.objects.all().count(), farts)

        self.fart3.created = self.fart3.created - datetime.timedelta(days=10000)
        self.fart3.save(force_modification=True)

        response = c.get('/login/{0}/'.format(self.fart3.uuid))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(c.session['_auth_user_id'], 1)

        self.assertEqual(FART.objects.all().count(), farts)

    def test_fart_login_view_with_session_data(self):
        c = Client()
        farts = FART.objects.all().count()

        response = c.get('/login/{0}/'.format(self.fart4.uuid))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(c.session['_auth_user_id'], 1)
        self.assertEqual(c.session['data'], "test")


class TestFARTMiddleware(TestFARTBase):
    def test_fart_login_middleware_not_valid(self):
        c = Client()
        false_uuid = '12341234-1234-1234-1234-123412341234'
        response = c.get('/test_url/', {'uuid-login': false_uuid})
        self.assertEqual(response.status_code, 200)
        self.assertFalse("_auth_user_id" in c.session)

    def test_fart_login_middleware_one_time(self):
        c = Client()
        farts = FART.objects.all().count()
        response = c.get('/test_url/', {'uuid-login': self.fart1.uuid})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(c.session['_auth_user_id'], 1)

        self.assertEqual(FART.objects.all().count(), farts-1)

        c.logout()
        self.assertFalse("_auth_user_id" in c.session)

        response = c.get('/test_url/', {'uuid-login': self.fart1.uuid})
        self.assertEqual(response.status_code, 200)
        self.assertFalse("_auth_user_id" in c.session)

        self.assertEqual(FART.objects.all().count(), farts-1)

    def test_fart_login_middleware_temporary_valid(self):
        c = Client()
        farts = FART.objects.all().count()
        response = c.get('/test_url/', {'uuid-login': self.fart2.uuid})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(c.session['_auth_user_id'], 1)

        self.assertEqual(FART.objects.all().count(), farts)

        c.logout()
        self.assertFalse("_auth_user_id" in c.session)

        self.fart2.created = self.fart2.created - datetime.timedelta(days=10)
        self.fart2.save(force_modification=True)

        response = c.get('/test_url/', {'uuid-login': self.fart2.uuid})
        self.assertEqual(response.status_code, 200)
        self.assertFalse("_auth_user_id" in c.session)

        self.assertEqual(FART.objects.all().count(), farts-1)

    def test_fart_login_middleware_allways_valid(self):
        c = Client()
        farts = FART.objects.all().count()

        response = c.get('/test_url/', {'uuid-login': self.fart3.uuid})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(c.session['_auth_user_id'], 1)

        c.logout()
        self.assertFalse("_auth_user_id" in c.session)

        self.assertEqual(FART.objects.all().count(), farts)

        response = c.get('/test_url/', {'uuid-login': self.fart3.uuid})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(c.session['_auth_user_id'], 1)

        c.logout()
        self.assertFalse("_auth_user_id" in c.session)

        self.assertEqual(FART.objects.all().count(), farts)

        self.fart3.created = self.fart3.created - datetime.timedelta(days=10000)
        self.fart3.save(force_modification=True)

        response = c.get('/test_url/', {'uuid-login': self.fart3.uuid})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(c.session['_auth_user_id'], 1)

        self.assertEqual(FART.objects.all().count(), farts)

    def test_fart_login_middleware_with_session_data(self):
        c = Client()
        farts = FART.objects.all().count()

        response = c.get('/test_url/', {'uuid-login': self.fart4.uuid})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(c.session['_auth_user_id'], 1)
        self.assertEqual(c.session['data'], "test")


class TestFARTModel(TestFARTBase):
    def test_fart_model_verify(self):
        self.assertTrue(self.fart1.verify())
        self.assertTrue(self.fart2.verify())
        self.assertTrue(self.fart3.verify())

        self.fart1.created = self.fart1.created - datetime.timedelta(seconds=100)
        self.fart2.created = self.fart2.created - datetime.timedelta(seconds=100)
        self.fart3.created = self.fart3.created - datetime.timedelta(seconds=100)

        self.assertFalse(self.fart1.verify())
        self.assertTrue(self.fart2.verify())
        self.assertTrue(self.fart3.verify())

        self.fart1.created = self.fart1.created - datetime.timedelta(days=10)
        self.fart2.created = self.fart2.created - datetime.timedelta(days=10)
        self.fart3.created = self.fart3.created - datetime.timedelta(days=10)

        self.assertFalse(self.fart1.verify())
        self.assertFalse(self.fart2.verify())
        self.assertTrue(self.fart3.verify())

        self.fart1.created = self.fart1.created - datetime.timedelta(days=10000)
        self.fart2.created = self.fart2.created - datetime.timedelta(days=10000)
        self.fart3.created = self.fart3.created - datetime.timedelta(days=10000)

        self.assertFalse(self.fart1.verify())
        self.assertFalse(self.fart2.verify())
        self.assertTrue(self.fart3.verify())

    def test_fart_model_is_one_time(self):
        self.assertTrue(self.fart1.is_one_time())
        self.assertFalse(self.fart2.is_one_time())
        self.assertFalse(self.fart3.is_one_time())
        self.assertFalse(self.fart4.is_one_time())
