# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0005_delete_my'),
    ]

    operations = [
        migrations.CreateModel(
            name='Changed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('change', models.BooleanField()),
            ],
        ),
    ]
