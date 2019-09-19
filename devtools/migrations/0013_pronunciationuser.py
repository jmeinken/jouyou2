# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-10 00:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('devtools', '0012_worddeleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='PronunciationUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pronunciation', models.CharField(max_length=10)),
                ('mnemonic', models.CharField(blank=True, max_length=500, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]