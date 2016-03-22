# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0002_frontpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='frontpage',
            name='frontpage_url',
            field=models.CharField(default='a', max_length=200),
            preserve_default=False,
        ),
    ]
