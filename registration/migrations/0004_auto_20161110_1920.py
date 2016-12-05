# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20161110_1752'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='Interests',
            new_name='interests',
        ),
        migrations.RenameField(
            model_name='myuser',
            old_name='PostCode',
            new_name='postCode',
        ),
    ]
