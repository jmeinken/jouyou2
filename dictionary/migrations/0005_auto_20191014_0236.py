# Generated by Django 2.2.5 on 2019-10-14 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0004_auto_20191014_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radical',
            name='meaning',
            field=models.TextField(blank=True, null=True),
        ),
    ]