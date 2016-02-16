# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-06 07:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0008_auto_20160205_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='created_by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='university.Employee'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='billtype',
            name='generation_day',
            field=models.IntegerField(default=1),
        ),
    ]
