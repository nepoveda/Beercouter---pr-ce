# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-11 08:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beercounter', '0014_auto_20170623_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Cena'),
        ),
    ]