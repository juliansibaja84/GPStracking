# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-07 02:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('historic', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='truck',
            name='log',
        ),
        migrations.DeleteModel(
            name='Logs',
        ),
    ]