# Generated by Django 2.2.5 on 2019-09-22 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0002_conceptuser_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conceptuser',
            name='concept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dictionary.LearnableConcept'),
        ),
    ]