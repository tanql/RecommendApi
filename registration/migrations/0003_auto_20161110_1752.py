# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20161110_1751'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='PostalCode',
            new_name='PostCode',
        ),
    ]
