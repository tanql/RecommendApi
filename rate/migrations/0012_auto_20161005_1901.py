# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0011_auto_20161005_1846'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='movieGenre',
        ),
        migrations.AddField(
            model_name='movie',
            name='movieGenre',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
    ]
