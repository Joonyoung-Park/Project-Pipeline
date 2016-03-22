# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0003_frontpage_frontpage_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='pipeline',
            name='project_team',
            field=models.CharField(default='vcrm_planning_team', max_length=200),
            preserve_default=False,
        ),
    ]
