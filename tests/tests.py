import json
import datetime

from django.utils import unittest
from django.conf import settings
from django.template import Template, Context
from django.core.management import call_command
from django.test.client import Client
from django.views.generic import View
from django.http import HttpResponse

from django.contrib.auth import get_user_model

from lot.models import LOT
import lot.models

call_command('syncdb', interactive=False)

class TestView(View):
    def get(self, request):
        return HttpResponse()


class TestLOTBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        get_user_model().objects.all().delete()
        LOT.objects.all().delete()

        test_user = get_user_model().objects.create(username="test")
        cls.lot1 = LOT.objects.create(
            user=test_user,
            type="fast-login",
        )
        cls.lot2 = LOT.objects.create(
            user=test_user,
            type="slow-login",
        )
        cls.lot3 = LOT.objects.create(
            user=test_user,
            type="always-login",
        )
        cls.lot4 = LOT.objects.create(
            user=test_user,
            type="always-login",
            session_data=json.dumps({'data':'test'}),
        )

        lot.models.LOT_SETTINGS['with-session-data-login'] = {
            'name': 'with session data login',
            'one-time': False,
            'duration': None,
            'verify-func': lambda x: len(x.session_data) != 0,
            'delete-on-fail': False
        }
        cls.lot5 = LOT.objects.create(
            user=test_user,
            type="with-session-data-login",
        )


class TestLOTView(TestLOTBase):
    def test_lot_login_view_not_valid(self):
        c = Client()
        false_uuid = '12341234-1234-1234-1234-123412341234'
        response = c.get('/login/{0}/'.format(false_uuid))
        self.assertEqual(response.status_code, 404)

    def test_lot_login_view_one_time(self):
        c = Client()
        lots = LOT.objects.all().count()
        response = c.get('/login/{0}/'.format(self.lot1.uuid))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(c.session['_auth_user_id'], 1)

        self.assertEqual(LOT.objects.all().count(), lots-1)

        response = c.get('/login/{0}/'.format(self.lot1.uuid))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(c.session['_auth_user_id'], 1)

        self.assertEqual(LOT.objects.all().count(), lots-1)

    def test_lot_login_view_temporary_valid(self):
        c = Client()
        lots = LOT.objects.all().count()
        response = c.get('/login/{0}/'.format(self.lot2.uuid))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(c.session['_auth_user_id'], 1)

        self.assertEqual(LOT.objects.all().count(), lots)

        c.logout()
        self.assertFalse("_auth_user_id" in c.session)

        self.lot2.created = self.lot2.created - datetime.timedelta(days=10)
        self.lot2.save(force_modification=True)

        response = c.get('/login/{0}/'.format(self.lot2.uuid))
        self.assertEqual(response.status_code, 404)
        self.assertFalse("_auth_user_id" in c.session)

        self.assertEqual(LOT.objects.all().count(), lots-1)

    def test_lot_login_view_allways_valid(self):
        c = Client()
        lots = LOT.objects.all().count()

        response = c.get('/login/{0}/'.format(self.lot3.uuid))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(c.session['_auth_user_id'], 1)

        c.logout()
        self.assertFalse("_auth_user_id" in c.session)

        self.assertEqual(LOT.objects.all().count(), lots)

        response = c.get('/login/{0}/'.format(self.lot3.uuid))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(c.session['_auth_user_id'], 1)

        c.logout()
        self.assertFalse("_auth_user_id" in c.session)

        self.assertEqual(LOT.objects.all().count(), lots)

        self.lot3.created = self.lot3.created - datetime.timedelta(days=10000)
        self.lot3.save(force_modification=True)

        response = c.get('/login/{0}/'.format(self.lot3.uuid))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(c.session['_auth_user_id'], 1)

        self.assertEqual(LOT.objects.all().count(), lots)

    def test_lot_login_view_with_session_data(self):
        c = Client()
        lots = LOT.objects.all().count()

        response = c.get('/login/{0}/'.format(self.lot4.uuid))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(c.session['_auth_user_id'], 1)
        self.assertEqual(c.session['data'], "test")


class TestLOTMiddleware(TestLOTBase):
    def test_lot_login_middleware_not_valid(self):
        c = Client()
        false_uuid = '12341234-1234-1234-1234-123412341234'
        response = c.get('/test_url/', {'uuid-login': false_uuid})
        self.assertEqual(response.status_code, 200)
        self.assertFalse("_auth_user_id" in c.session)

    def test_lot_login_middleware_one_time(self):
        c = Client()
        lots = LOT.objects.all().count()
        response = c.get('/test_url/', {'uuid-login': self.lot1.uuid})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(c.session['_auth_user_id'], 1)

        self.assertEqual(LOT.objects.all().count(), lots-1)

        c.logout()
        self.assertFalse("_auth_user_id" in c.session)

        response = c.get('/test_url/', {'uuid-login': self.lot1.uuid})
        self.assertEqual(response.status_code, 200)
        self.assertFalse("_auth_user_id" in c.session)

        self.assertEqual(LOT.objects.all().count(), lots-1)

    def test_lot_login_middleware_temporary_valid(self):
        c = Client()
        lots = LOT.objects.all().count()
        response = c.get('/test_url/', {'uuid-login': self.lot2.uuid})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(c.session['_auth_user_id'], 1)

        self.assertEqual(LOT.objects.all().count(), lots)

        c.logout()
        self.assertFalse("_auth_user_id" in c.session)

        self.lot2.created = self.lot2.created - datetime.timedelta(days=10)
        self.lot2.save(force_modification=True)

        response = c.get('/test_url/', {'uuid-login': self.lot2.uuid})
        self.assertEqual(response.status_code, 200)
        self.assertFalse("_auth_user_id" in c.session)

        self.assertEqual(LOT.objects.all().count(), lots-1)

    def test_lot_login_middleware_allways_valid(self):
        c = Client()
        lots = LOT.objects.all().count()

        response = c.get('/test_url/', {'uuid-login': self.lot3.uuid})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(c.session['_auth_user_id'], 1)

        c.logout()
        self.assertFalse("_auth_user_id" in c.session)

        self.assertEqual(LOT.objects.all().count(), lots)

        response = c.get('/test_url/', {'uuid-login': self.lot3.uuid})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(c.session['_auth_user_id'], 1)

        c.logout()
        self.assertFalse("_auth_user_id" in c.session)

        self.assertEqual(LOT.objects.all().count(), lots)

        self.lot3.created = self.lot3.created - datetime.timedelta(days=10000)
        self.lot3.save(force_modification=True)

        response = c.get('/test_url/', {'uuid-login': self.lot3.uuid})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(c.session['_auth_user_id'], 1)

        self.assertEqual(LOT.objects.all().count(), lots)

    def test_lot_login_middleware_with_session_data(self):
        c = Client()
        lots = LOT.objects.all().count()

        response = c.get('/test_url/', {'uuid-login': self.lot4.uuid})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(c.session['_auth_user_id'], 1)
        self.assertEqual(c.session['data'], "test")


class TestLOTModel(TestLOTBase):
    def test_lot_model_verify(self):
        self.assertTrue(self.lot1.verify())
        self.assertTrue(self.lot2.verify())
        self.assertTrue(self.lot3.verify())

        self.lot1.created = self.lot1.created - datetime.timedelta(seconds=100)
        self.lot2.created = self.lot2.created - datetime.timedelta(seconds=100)
        self.lot3.created = self.lot3.created - datetime.timedelta(seconds=100)

        self.assertFalse(self.lot1.verify())
        self.assertTrue(self.lot2.verify())
        self.assertTrue(self.lot3.verify())

        self.lot1.created = self.lot1.created - datetime.timedelta(days=10)
        self.lot2.created = self.lot2.created - datetime.timedelta(days=10)
        self.lot3.created = self.lot3.created - datetime.timedelta(days=10)

        self.assertFalse(self.lot1.verify())
        self.assertFalse(self.lot2.verify())
        self.assertTrue(self.lot3.verify())

        self.lot1.created = self.lot1.created - datetime.timedelta(days=10000)
        self.lot2.created = self.lot2.created - datetime.timedelta(days=10000)
        self.lot3.created = self.lot3.created - datetime.timedelta(days=10000)

        self.assertFalse(self.lot1.verify())
        self.assertFalse(self.lot2.verify())
        self.assertTrue(self.lot3.verify())

        # Testing verify func on LOT configuration
        self.assertFalse(self.lot5.verify())
        self.lot5.session_data = "test"
        self.assertTrue(self.lot5.verify())

    def test_lot_model_is_one_time(self):
        self.assertTrue(self.lot1.is_one_time())
        self.assertFalse(self.lot2.is_one_time())
        self.assertFalse(self.lot3.is_one_time())
        self.assertFalse(self.lot4.is_one_time())

    def test_lot_model_delete_on_fail(self):
        self.assertTrue(self.lot1.delete_on_fail())
        self.assertTrue(self.lot2.delete_on_fail())
        self.assertTrue(self.lot3.delete_on_fail())
        self.assertTrue(self.lot4.delete_on_fail())
        self.assertFalse(self.lot5.delete_on_fail())
