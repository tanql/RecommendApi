# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='movieName',
            field=models.CharField(default=0, max_length=120),
            preserve_default=False,
        ),
    ]
