import simplejson

from django.conf import settings
from django.contrib.auth import authenticate, login

from .models import LOT

class LOTMiddleware(object):
    def process_request(self, request):
        lot_uuid = request.GET.get(settings.LOT_MIDDLEWARE_PARAM_NAME, None)
        if lot_uuid:
            try:
                lot = LOT.objects.get(uuid=lot_uuid)
            except LOT.DoesNotExist:
                return None

            if not lot.verify():
                lot.delete()
                return None

            user = authenticate(lot_uuid=lot_uuid)
            login(request, user)

            try:
                session_data = simplejson.loads(lot.session_data)
                for key, value in session_data.iteritems():
                    request.session[key] = value
            except Exception:
                # If not correctly serialized not set the session_data
                pass

            if lot.is_one_time():
                lot.delete()
