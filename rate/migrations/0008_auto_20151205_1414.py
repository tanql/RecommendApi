# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0007_delete_changed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('genre', models.CharField(max_length=120)),
            ],
        ),
        migrations.AddField(
            model_name='rating',
            name='movieGenre',
            field=models.ManyToManyField(to='rate.Genre'),
        ),
    ]
