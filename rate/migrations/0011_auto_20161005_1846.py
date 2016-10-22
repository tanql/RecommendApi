# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0010_auto_20161005_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='movieId',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='rating',
            name='movie',
            field=models.ForeignKey(to='rate.Movie'),
        ),
    ]
