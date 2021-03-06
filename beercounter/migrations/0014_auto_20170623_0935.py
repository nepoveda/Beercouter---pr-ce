# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-23 07:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beercounter', '0013_auto_20170621_1657'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bill',
            options={'verbose_name': '\xda\u010det'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': 'Polo\u017eka'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Objedn\xe1vka'},
        ),
        migrations.AlterModelOptions(
            name='pub',
            options={'verbose_name': 'Hospoda'},
        ),
        migrations.AlterField(
            model_name='order',
            name='bill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='beercounter.Bill', verbose_name='\xda\u010det'),
        ),
        migrations.AlterField(
            model_name='order',
            name='count',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Po\u010det'),
        ),
        migrations.AlterField(
            model_name='order',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='beercounter.Item', verbose_name='Polo\u017eka'),
        ),
    ]
