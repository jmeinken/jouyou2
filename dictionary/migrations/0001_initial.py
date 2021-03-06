# Generated by Django 2.2.5 on 2019-09-20 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kanji',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.CharField(max_length=1, unique=True)),
                ('meaning', models.CharField(blank=True, max_length=255, null=True)),
                ('main_pronunciation', models.CharField(blank=True, max_length=10, null=True)),
                ('stroke_count', models.IntegerField(blank=True, null=True)),
                ('grade', models.IntegerField(blank=True, null=True)),
                ('popularity', models.IntegerField(blank=True, null=True)),
                ('jlpt_level', models.IntegerField(blank=True, null=True)),
                ('hybrid_order', models.IntegerField(blank=True, null=True)),
                ('comment', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LearnableConcept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('character', 'character'), ('word', 'word')], max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=50)),
                ('definition', models.TextField()),
                ('pronunciation', models.CharField(blank=True, max_length=50, null=True)),
                ('pronunciation_array', models.TextField(default='[]')),
                ('is_proper_noun', models.BooleanField(default=False)),
                ('popularity', models.IntegerField(blank=True, null=True)),
                ('concept', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dictionary.LearnableConcept')),
                ('kanji_set', models.ManyToManyField(blank=True, to='dictionary.Kanji')),
            ],
        ),
        migrations.CreateModel(
            name='Radical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.CharField(max_length=1, unique=True)),
                ('meaning', models.CharField(blank=True, max_length=255, null=True)),
                ('stroke_count', models.IntegerField(blank=True, null=True)),
                ('identical_kanji', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dictionary.Kanji')),
            ],
        ),
        migrations.CreateModel(
            name='Pronunciation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('on-yomi', 'on-yomi'), ('kun-yomi', 'kun-yomi')], max_length=10)),
                ('pronunciation', models.CharField(max_length=10)),
                ('kanji', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionary.Kanji')),
            ],
        ),
        migrations.AddField(
            model_name='kanji',
            name='concept',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dictionary.LearnableConcept'),
        ),
        migrations.AddField(
            model_name='kanji',
            name='radicals',
            field=models.ManyToManyField(blank=True, to='dictionary.Radical'),
        ),
    ]
