# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='next_url',
            field=models.URLField(blank=True),
        ),
    ]
