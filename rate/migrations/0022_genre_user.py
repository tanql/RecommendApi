# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0011_myuser'),
        ('rate', '0021_rating_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='user',
            field=models.ManyToManyField(to='registration.MyUser'),
        ),
    ]
