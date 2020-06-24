# Generated by Django 3.0.7 on 2020-06-24 03:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20200620_1228'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=256, unique=True)),
                ('uses', models.IntegerField()),
                ('expiry_date', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Quiz')),
            ],
            options={
                'verbose_name': 'Quiz Code',
                'verbose_name_plural': 'Quiz Codes',
            },
        ),
    ]