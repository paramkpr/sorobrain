# Generated by Django 3.1 on 2020-09-27 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0006_auto_20200826_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='hide_leaderboard',
            field=models.BooleanField(default=False, verbose_name='Hide Leader-board'),
        ),
    ]
