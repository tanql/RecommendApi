# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0008_auto_20151205_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('movieName', models.CharField(max_length=120)),
                ('movieGenre', models.ManyToManyField(to='rate.Genre')),
            ],
        ),
        migrations.RemoveField(
            model_name='rating',
            name='movieGenre',
        ),
    ]
