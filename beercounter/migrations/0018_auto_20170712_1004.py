# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-12 08:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('beercounter', '0017_auto_20170711_1156'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pub',
            options={'ordering': ('name',), 'verbose_name': 'Hospoda'},
        ),
        migrations.AddField(
            model_name='bill',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bills', to=settings.AUTH_USER_MODEL),
        ),
    ]
