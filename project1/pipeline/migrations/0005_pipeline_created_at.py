# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0004_pipeline_project_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='pipeline',
            name='created_at',
            field=models.DateTimeField(default=datetime.date(2016, 3, 23), auto_now_add=True),
            preserve_default=False,
        ),
    ]
