# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0017_auto_20161013_1148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='userId',
        ),
    ]
