from django.contrib.auth.backends import ModelBackend

from .models import LOT


class LOTBackend(ModelBackend):
    def authenticate(self, lot_uuid=None, **kwargs):
        try:
            lot = LOT.objects.get(uuid=lot_uuid)
        except LOT.DoesNotExist:
            return None
        return lot.user
