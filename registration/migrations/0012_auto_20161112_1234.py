# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0011_myuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='postCode',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
