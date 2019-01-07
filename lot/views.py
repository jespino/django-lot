import json

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404, resolve_url
from django.utils.http import is_safe_url
from django.views.generic import View

from django.contrib.auth import authenticate, login

from .models import LOT


class LOTLogin(View):
    def get(self, request, uuid):
        lot = get_object_or_404(LOT, uuid=uuid)
        if not lot.verify():
            lot.delete()
            return HttpResponseNotFound()

        user = authenticate(request, lot_uuid=uuid)
        if user is not None:
            login(request, user)
        else:
            raise RuntimeError('The authentication backend did not return a user')

        try:
            session_data = json.loads(lot.session_data)
            request.session.update(session_data)
        except Exception:
            # If not correctly serialized not set the session_data
            pass

        if lot.is_one_time():
            lot.delete()

        redirect_to = request.GET.get('next')
        if lot.next_url:
            redirect_to = resolve_url(lot.next_url)

        if not is_safe_url(url=redirect_to, allowed_hosts=[request.get_host()]):
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

        return HttpResponseRedirect(redirect_to)
