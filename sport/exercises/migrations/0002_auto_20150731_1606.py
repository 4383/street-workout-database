# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='equipment',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='muscle',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='musclegroup',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='muscletype',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='step',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='image',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
