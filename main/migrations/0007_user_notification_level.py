# Generated by Django 3.0.5 on 2020-05-18 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20200518_0535'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='notification_level',
            field=models.IntegerField(default='4', verbose_name='Notification Level'),
        ),
    ]
