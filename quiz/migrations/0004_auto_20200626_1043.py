# Generated by Django 3.0.7 on 2020-06-26 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_quizcode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quizsubmission',
            old_name='creation_time',
            new_name='created_on',
        ),
    ]
