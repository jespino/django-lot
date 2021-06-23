import json
from uuid import UUID
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.utils.deprecation import MiddlewareMixin

from .models import LOT


class LOTMiddleware(MiddlewareMixin):
    def process_request(self, request):
        lot_uuid = request.GET.get(settings.LOT_MIDDLEWARE_PARAM_NAME, None)
        if lot_uuid:
            try:
                val = UUID(lot_uuid, version=4)
            except ValueError:
                return None

            try:
                lot = LOT.objects.get(uuid=str(val))
            except LOT.DoesNotExist:
                return None

            if not lot.verify():
                if lot.delete_on_fail():
                    lot.delete()
                return None

            user = authenticate(lot_uuid=lot_uuid)
            login(request, user)

            try:
                session_data = json.loads(lot.session_data)
                request.session.update(session_data)
            except Exception:
                # If not correctly serialized not set the session_data
                pass

            if lot.is_one_time():
                lot.delete()


class LOTAuthenticationMiddleware(MiddlewareMixin):
    '''Authenticate using a Header'''
    def process_request(self, request):
        try:
            token = request.META['HTTP_X_AUTH_TOKEN']
        except KeyError:
            return None

        if not uuidRegex.match(token):
            return None

        try:
            lot = LOT.objects.select_related('user').get(uuid=token)
        except LOT.DoesNotExist:
            return None

        if not lot.verify():
            if lot.delete_on_fail():
                lot.delete()
            return None

        request.user = lot.user

        try:
            session_data = json.loads(lot.session_data)
            request.session.update(session_data)
        except:
            pass

        if lot.is_one_time():
            lot.delete()
