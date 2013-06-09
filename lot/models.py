import datetime
from uuid import uuid4

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model

from django.utils.timezone import now

LOT_SETTINGS = getattr(settings, 'LOT', {
    'fast-login': {
        'name': _(u'Fast login'),
        'duration': 60,
        'one-time': True,
    },
    'slow-login': {
        'name': _(u'Slow login'),
        'duration': 60*60*24,
        'one-time': False
    },
    'always-login': {
        'name': _(u'Always login'),
        'one-time': False,
        'duration': None,
    },
})
LOT_TYPE_CHOICES = [ (key, value['name']) for key, value in LOT_SETTINGS.iteritems() ]

class LOT(models.Model):
    uuid = models.CharField(max_length=50, null=False, blank=False, verbose_name=_('Uuid'))
    type = models.SlugField(max_length=50, choices=LOT_TYPE_CHOICES, null=False, blank=False, verbose_name=_('LOT type'))
    user = models.ForeignKey(get_user_model(), null=False, blank=False, verbose_name=_('user'))
    session_data = models.TextField(null=True, blank=True, verbose_name=_('Jsoned Session Data'))
    created = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name=_('creation date'))

    def verify(self):
        if not self.type in LOT_SETTINGS:
            return False

        duration = LOT_SETTINGS.get(self.type).get('duration', None)

        if duration == None:
            return True
        else:
            return (now() - self.created).total_seconds() < duration

    def is_one_time(self):
        return LOT_SETTINGS.get(self.type, {}).get('one-time', False)

    def save(self, *args, **kwargs):
        if self.id and not kwargs.pop('force_modification', False):
            raise Exception('Modification not allowed (you can force it with the force_modification parameter on save)')
        self.uuid = uuid4()
        super(LOT, self).save(*args, **kwargs)
