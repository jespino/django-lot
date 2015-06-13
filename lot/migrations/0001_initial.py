# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LOT',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('uuid', models.CharField(max_length=50, verbose_name='UUID')),
                ('type', models.SlugField(choices=[('fast-login', 'Fast login')], verbose_name='LOT type')),
                ('session_data', models.TextField(verbose_name='Jsoned Session Data', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
