# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-13 07:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beercounter', '0003_auto_20170612_2049'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='order',
            unique_together=set([('bill', 'item')]),
        ),
    ]
