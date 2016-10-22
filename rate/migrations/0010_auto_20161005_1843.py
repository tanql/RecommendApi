# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0009_auto_20151207_1359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='movieId',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='movieName',
        ),
        migrations.AddField(
            model_name='movie',
            name='movieId',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='rating',
            name='movie',
            field=models.ForeignKey(to='rate.Movie', null=True),
        ),
    ]
