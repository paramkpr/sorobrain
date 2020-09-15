# Generated by Django 3.1 on 2020-09-15 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20200626_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.CharField(help_text="any of the following: T, F, 1, 2, 3, 4 or some text. For text answers separate multiple correct choices with '|' (pipe) character.", max_length=1024, verbose_name='Answer'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='thumbnail',
            field=models.ImageField(blank=True, default='quiz/thumbnails/quiz-placeholder.jpg', null=True, upload_to='quiz/thumbnails/'),
        ),
    ]
