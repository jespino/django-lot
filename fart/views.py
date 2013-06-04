import simplejson

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import View

from django.contrib.auth import authenticate, login

from .models import FART

class FARTLogin(View):
    def get(self, request, uuid):
        next_url = request.GET.get('next', '/')
        fart = get_object_or_404(FART, uuid=uuid)
        if not fart.verify():
            fart.delete()
            return HttpResponseNotFound()

        user = authenticate(fart_uuid=uuid)
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

        return HttpResponseRedirect(next_url)
