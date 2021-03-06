# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 07:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('count', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.PositiveSmallIntegerField(default=0)),
                ('category', models.CharField(choices=[('D', 'N\xe1poje'), ('F', 'J\xeddlo'), ('O', 'Ostatn\xed')], default='D', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveSmallIntegerField(default=0)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bill', to='beercounter.Bill')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='beercounter.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Pub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Hospoda', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='pub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='beercounter.Pub'),
        ),
        migrations.AddField(
            model_name='bill',
            name='pub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to='beercounter.Pub'),
        ),
    ]
