# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-13 14:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beercounter', '0005_auto_20170613_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('N', 'N\xe1poje'), ('J', 'J\xeddlo'), ('O', 'Ostatn\xed')], default='J', max_length=1, verbose_name='Kategorie'),
        ),
    ]
