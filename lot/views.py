import simplejson

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import View

from django.contrib.auth import authenticate, login

from .models import LOT

class LOTLogin(View):
    def get(self, request, uuid):
        next_url = request.GET.get('next', '/')
        lot = get_object_or_404(LOT, uuid=uuid)
        if not lot.verify():
            lot.delete()
            return HttpResponseNotFound()

        user = authenticate(lot_uuid=uuid)
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

        return HttpResponseRedirect(next_url)
