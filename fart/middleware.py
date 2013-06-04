import simplejson

from django.conf import settings
from django.contrib.auth import authenticate, login

from .models import FART

class FartMiddleware(object):
    def process_request(self, request):
        fart_uuid = request.GET.get(settings.FART_MIDDLEWARE_PARAM_NAME, None)
        if fart_uuid:
            try:
                fart = FART.objects.get(uuid=fart_uuid)
            except FART.DoesNotExist:
                return None

            if not fart.verify():
                fart.delete()
                return None

            user = authenticate(fart_uuid=fart_uuid)
            login(request, user)

            try:
                session_data = simplejson.loads(fart.session_data)
                for key, value in session_data.iteritems():
                    request.session[key] = value
            except Exception:
                # If not correctly serialized not set the session_data
                pass

            if fart.is_one_time():
                fart.delete()
