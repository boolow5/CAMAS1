# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0002_auto_20160203_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='subjects',
            field=models.ManyToManyField(null=True, to='university.Subject'),
        ),
    ]
