# Generated by Django 2.2.5 on 2019-09-21 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conceptuser',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]