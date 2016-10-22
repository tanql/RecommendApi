# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0006_changed'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Changed',
        ),
    ]
