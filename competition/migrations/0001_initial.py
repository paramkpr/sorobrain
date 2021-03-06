# Generated by Django 3.0.7 on 2020-06-20 06:58

import ckeditor_uploader.fields
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0001_initial'),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.IntegerField()),
                ('discount', models.IntegerField(blank=True, null=True, verbose_name='Discount Percentage')),
                ('group_cost', models.IntegerField()),
                ('title', models.CharField(max_length=256)),
                ('slug', models.SlugField(blank=True, max_length=256, unique_for_date=True, verbose_name='Slug')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('level', models.CharField(choices=[(None, ''), ('fluent', 'Fluent/Native Speaker'), ('advanced', 'Advanced'), ('intermediate', 'Intermediate'), ('beginner', 'Beginner')], max_length=128, verbose_name='French Level')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='compete/thumbnails/')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('result', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created On')),
            ],
            options={
                'verbose_name': 'Competition',
                'verbose_name_plural': 'Competitions',
            },
        ),
        migrations.CreateModel(
            name='CompetitionQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.Competition')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Quiz')),
            ],
            options={
                'ordering': ('created_on',),
            },
        ),
        migrations.CreateModel(
            name='CompetitionCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=256, unique=True)),
                ('uses', models.IntegerField()),
                ('expiry_date', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.Competition')),
            ],
            options={
                'verbose_name': 'Competition Code',
                'verbose_name_plural': 'Competition Codes',
            },
        ),
        migrations.AddField(
            model_name='competition',
            name='quizzes',
            field=models.ManyToManyField(through='competition.CompetitionQuiz', to='quiz.Quiz'),
        ),
        migrations.AddField(
            model_name='competition',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='CompetitionAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.Competition')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Competition Access',
                'verbose_name_plural': 'Competition Accesses',
                'ordering': ('-created_on', 'competition'),
                'unique_together': {('user', 'competition')},
            },
        ),
    ]
