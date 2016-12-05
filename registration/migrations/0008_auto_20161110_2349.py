# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0007_auto_20161110_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='interests',
            field=django.contrib.postgres.fields.ArrayField(size=None, null=True, base_field=models.CharField(max_length=200), blank=True),
        ),
    ]
