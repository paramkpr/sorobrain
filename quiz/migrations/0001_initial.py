# Generated by Django 3.0.7 on 2020-06-19 11:43

import ckeditor_uploader.fields
import datetime
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.IntegerField()),
                ('discount', models.IntegerField(blank=True, null=True, verbose_name='Discount Percentage')),
                ('title', models.CharField(max_length=256, verbose_name='Quiz Title')),
                ('slug', models.SlugField(blank=True, max_length=256, unique_for_date=True, verbose_name='Slug')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('level', models.CharField(choices=[(None, ''), ('fluent', 'Fluent/Native Speaker'), ('advanced', 'Advanced'), ('intermediate', 'Intermediate'), ('beginner', 'Beginner')], max_length=128, verbose_name='French Level')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='quiz/thumbnails/')),
                ('total_time', models.DurationField(default=datetime.timedelta(seconds=900), verbose_name='Total Time')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Quiz Created On')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quizzes',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='QuizSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission', django.contrib.postgres.fields.jsonb.JSONField(default=dict, null=True)),
                ('score', models.FloatField(null=True)),
                ('correct_answers', models.IntegerField(null=True)),
                ('incorrect_answers', models.IntegerField(null=True)),
                ('start_time', models.DateTimeField()),
                ('submit_time', models.DateTimeField(null=True)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_submission_quiz', to='quiz.Quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Quiz Submission',
                'verbose_name_plural': 'Quiz Submissions',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', ckeditor_uploader.fields.RichTextUploadingField()),
                ('explanation', ckeditor_uploader.fields.RichTextUploadingField()),
                ('type', models.CharField(choices=[('mcq', 'Multiple Choice Question'), ('bool', 'True or False'), ('text', 'Text Answer')], max_length=32)),
                ('option1', models.CharField(blank=True, max_length=512, null=True)),
                ('option2', models.CharField(blank=True, max_length=512, null=True)),
                ('option3', models.CharField(blank=True, max_length=512, null=True)),
                ('option4', models.CharField(blank=True, max_length=512, null=True)),
                ('answer', models.CharField(max_length=32, verbose_name='Answer: any of the following: T, F, 1, 2, 3, 4 or some text')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Quiz')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'ordering': ['created_on'],
            },
        ),
        migrations.CreateModel(
            name='QuizAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Quiz Access',
                'verbose_name_plural': 'Quiz Access',
                'ordering': ('quiz', '-created_on'),
                'unique_together': {('user', 'quiz')},
            },
        ),
    ]
