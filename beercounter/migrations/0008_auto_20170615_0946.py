# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-15 07:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beercounter', '0007_auto_20170614_1542'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='order',
            unique_together=set([]),
        ),
    ]