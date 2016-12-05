# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20161110_2315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='interests',
        ),
    ]
