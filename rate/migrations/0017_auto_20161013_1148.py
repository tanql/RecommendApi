# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0016_rating_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='movieName',
            field=models.CharField(max_length=200),
        ),
    ]
