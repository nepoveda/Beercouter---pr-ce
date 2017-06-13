# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-12 18:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beercounter', '0002_remove_bill_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Jm\xe9no'),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('D', 'N\xe1poje'), ('F', 'J\xeddlo'), ('O', 'Ostatn\xed')], default='D', max_length=1, verbose_name='Kategorie'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=51, unique=True, verbose_name='N\xe1zev'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Cena'),
        ),
        migrations.AlterField(
            model_name='item',
            name='pub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='beercounter.Pub', verbose_name='Hospoda'),
        ),
        migrations.AlterField(
            model_name='pub',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='N\xe1zev'),
        ),
        migrations.AlterUniqueTogether(
            name='bill',
            unique_together=set([('name', 'pub')]),
        ),
    ]
