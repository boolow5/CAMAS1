# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-12-26 17:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0012_errorreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='subject',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='university.Subject'),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='dean',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='university.Employee'),
        ),
    ]
