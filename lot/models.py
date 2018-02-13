from uuid import uuid4

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.core.exceptions import ValidationError


# Taken from mezzaine, Django < 1.5 compatability
# https://github.com/stephenmcd/mezzanine/blob/master/mezzanine/utils/models.py
user_model_name = getattr(settings, "AUTH_USER_MODEL", "auth.User")


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
LOT_TYPE_CHOICES = [
    (key, value['name'])
    for key, value in LOT_SETTINGS.items()
]


class LOT(models.Model):
    uuid = models.CharField(_('UUID'), max_length=50)
    type = models.SlugField(_('LOT type'), max_length=50)
    user = models.ForeignKey(user_model_name, verbose_name=_('user'), on_delete=models.CASCADE)
    session_data = models.TextField(_('Jsoned Session Data'), blank=True)
    created = models.DateTimeField(_('Creation date'), auto_now_add=True)
    next_url = models.URLField(blank=True)

    def verify(self):
        if self.type not in LOT_SETTINGS:
            return False

        verify_setting = LOT_SETTINGS[self.type]

        duration = verify_setting.get('duration', None)
        verify_func = verify_setting.get('verify-func', lambda x: True)

        if not verify_func(self):
            return False

        if duration is None:
            return True

        dt = now() - self.created
        if hasattr(dt, 'total_seconds'):
            return (dt.total_seconds() < duration)
        else:
            return ((dt.microseconds + (dt.seconds + dt.days * 24 * 3600) * 10 ** 6) / 10 ** 6 < duration)

    def delete_on_fail(self):
        if self.type not in LOT_SETTINGS:
            return True

        return LOT_SETTINGS[self.type].get('delete-on-fail', True)

    def is_one_time(self):
        return LOT_SETTINGS.get(self.type, {}).get('one-time', False)

    def save(self, *args, **kwargs):
        self.uuid = uuid4()
        super(LOT, self).save(*args, **kwargs)

    def clean(self):
        if self.type not in LOT_SETTINGS:
            raise ValidationError(_('LOT type %s not found' % self.type))

    def __unicode__(self):
        return u"{0} ({1})".format(self.get_type_display(), self.uuid)
