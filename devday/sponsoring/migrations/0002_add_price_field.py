# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-23 15:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsoring', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsoringpackage',
            name='pricing',
            field=models.CharField(default='', max_length=10, verbose_name='Price'),
            preserve_default=False,
        ),
    ]
