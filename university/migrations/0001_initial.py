# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('number', models.IntegerField()),
                ('balance', models.DecimalField(max_digits=12, decimal_places=2, default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2, default=0.0)),
                ('description', models.TextField(max_length=300)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('account', models.ForeignKey(to='university.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=30, default='One')),
                ('date_opened', models.DateField(default=django.utils.timezone.now)),
                ('max_year', models.IntegerField(default=4)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('starting_date', models.DateField(default=django.utils.timezone.now)),
                ('is_admission', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ExamReport',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('grade', models.DecimalField(max_digits=5, decimal_places=2, default=0.0)),
                ('note', models.TextField()),
                ('exam', models.ForeignKey(to='university.Exam')),
            ],
        ),
        migrations.CreateModel(
            name='ExamType',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('max_marks', models.DecimalField(max_digits=5, decimal_places=2, default=100.0)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=200)),
                ('dean', models.ForeignKey(to='university.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('level', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('middle_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('DateOfBirth', models.DateField()),
                ('address', models.TextField(default=None)),
                ('phone', models.CharField(max_length=30)),
                ('guardian', models.CharField(max_length=50)),
                ('guardian_phone', models.CharField(max_length=30)),
                ('status', models.BooleanField(default=False)),
                ('registered', models.DateField(default=django.utils.timezone.now)),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('classroom', models.ForeignKey(to='university.Classroom')),
                ('registered_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('is_first', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2, default=0.0)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField(max_length=300)),
                ('is_debit', models.BooleanField(default=True)),
                ('payee', models.ForeignKey(to='university.Account')),
                ('received_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('level', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='examreport',
            name='student',
            field=models.ForeignKey(to='university.Student'),
        ),
        migrations.AddField(
            model_name='examreport',
            name='subject',
            field=models.ForeignKey(to='university.Subject'),
        ),
        migrations.AddField(
            model_name='exam',
            name='e_type',
            field=models.ForeignKey(to='university.ExamType'),
        ),
        migrations.AddField(
            model_name='employee',
            name='position',
            field=models.ForeignKey(to='university.Position', null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='subject',
            field=models.ForeignKey(to='university.Subject', default=None),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(to='university.Faculty'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='current_semester',
            field=models.ForeignKey(to='university.Term'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='current_year',
            field=models.ForeignKey(to='university.Year'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='department',
            field=models.ForeignKey(to='university.Department', null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='owner',
            field=models.ForeignKey(to='university.Student'),
        ),
    ]
