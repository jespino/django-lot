# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lot', '0002_lot_next_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='type',
            field=models.SlugField(verbose_name='LOT type'),
        ),
    ]
