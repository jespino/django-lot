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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(verbose_name='UUID', max_length=50)),
                ('type', models.SlugField(choices=[('fast-login', 'Fast login'), ('slow-login', 'Slow login'), ('always-login', 'Always login')], verbose_name='LOT type')),
                ('session_data', models.TextField(blank=True, verbose_name='Jsoned Session Data')),
                ('created', models.DateTimeField(verbose_name='Creation date', auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
    ]
