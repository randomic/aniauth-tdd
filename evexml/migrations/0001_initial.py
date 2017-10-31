# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 10:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APIKeyPair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_id', models.IntegerField(verbose_name=' keyID')),
                ('v_code', models.CharField(max_length=64, verbose_name=' vCode')),
                ('is_valid', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='apikeypair',
            unique_together=set([('key_id', 'v_code')]),
        ),
    ]