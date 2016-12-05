# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_remove_myuser_interests'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='age',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='interests',
            field=django.contrib.postgres.fields.ArrayField(null=True, base_field=models.CharField(max_length=10, null=True, blank=True), size=8),
        ),
        migrations.AddField(
            model_name='myuser',
            name='postCode',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
