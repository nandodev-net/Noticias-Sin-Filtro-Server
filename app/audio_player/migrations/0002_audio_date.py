# Generated by Django 4.0.2 on 2022-06-10 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio_player', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]