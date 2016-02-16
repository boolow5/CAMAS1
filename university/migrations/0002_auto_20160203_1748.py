# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='semester',
            field=models.ForeignKey(to='university.Term', null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='year',
            field=models.ForeignKey(to='university.Year', null=True),
        ),
    ]
