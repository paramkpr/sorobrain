# Generated by Django 3.0.5 on 2020-05-27 06:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workshops', '0003_auto_20200527_0237'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkshopAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workshop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshops.Workshop')),
            ],
            options={
                'verbose_name': 'Workshop Access',
                'verbose_name_plural': 'Workshop Accesses',
                'ordering': ('workshop', '-created_on'),
                'unique_together': {('user', 'workshop')},
            },
        ),
    ]
