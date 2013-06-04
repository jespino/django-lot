from django.contrib.auth.backends import ModelBackend

from .models import FART

class FARTBackend(ModelBackend):
    def authenticate(self, fart_uuid=None, **kwargs):
        try:
            fart = FART.objects.get(uuid=fart_uuid)
            user = fart.user
            return user
        except FART.DoesNotExist:
            return None
