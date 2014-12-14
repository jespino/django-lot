import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import View

from django.contrib.auth import authenticate, login

from .models import LOT


class LOTLogin(View):
    def get(self, request, uuid):
        print "wtf"
        next_url = request.GET.get('next', '/')
        print uuid
        lot = get_object_or_404(LOT, uuid=uuid)
        print lot
        print lot.verify()
        if not lot.verify():
            lot.delete()
            return HttpResponseNotFound()
        print "verified"
        user = authenticate(lot_uuid=uuid)
        login(request, user)
        print login
        try:
            session_data = json.loads(lot.session_data)
            request.session.update(session_data)
        except Exception:
            # If not correctly serialized not set the session_data
            pass

        if lot.is_one_time():
            lot.delete()
        print next_url
        return HttpResponseRedirect(next_url)
