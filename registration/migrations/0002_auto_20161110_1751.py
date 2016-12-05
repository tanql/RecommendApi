# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='Interests',
            field=models.CharField(max_length=120, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='PostalCode',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='age',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
