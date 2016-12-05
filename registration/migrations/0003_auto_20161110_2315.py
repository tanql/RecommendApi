# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20161110_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='interests',
            field=django.contrib.postgres.fields.ArrayField(null=True, base_field=models.CharField(max_length=10, null=True, blank=True), size=8),
        ),
    ]
