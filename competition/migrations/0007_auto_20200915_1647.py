# Generated by Django 3.1 on 2020-09-15 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0006_auto_20200826_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='result',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
