from uuid import uuid4

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except:
    from django.apps import apps
    user_app, user_model = settings.AUTH_USER_MODEL.split('.')
    User = apps.get_app_config(user_app).get_model(user_model)

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
LOT_TYPE_CHOICES = [
    (key, value['name'])
    for key, value in LOT_SETTINGS.items()
]


class LOT(models.Model):
    uuid = models.CharField(_('UUID'), max_length=50)
    type = models.SlugField(_('LOT type'), max_length=50,
                            choices=LOT_TYPE_CHOICES)
    user = models.ForeignKey(User, verbose_name=_('user'))
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

        return (now() - self.created).total_seconds() < duration

    def delete_on_fail(self):
        if self.type not in LOT_SETTINGS:
            return True

        return LOT_SETTINGS[self.type].get('delete-on-fail', True)

    def is_one_time(self):
        return LOT_SETTINGS.get(self.type, {}).get('one-time', False)

    def save(self, *args, **kwargs):
        if self.id and not kwargs.pop('force_modification', False):
            raise Exception('Modification not allowed without '
                            'force_modification parameter on save.')
        self.uuid = uuid4()
        super(LOT, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"{0} ({1})".format(self.get_type_display(), self.uuid)
