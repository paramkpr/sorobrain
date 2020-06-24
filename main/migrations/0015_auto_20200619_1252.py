# Generated by Django 3.0.5 on 2020-06-19 07:22

from django.db import migrations, models
import django.db.models.deletion
import gfklookupwidget.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('main', '0014_discountcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountcode',
            name='content_type',
            field=models.ForeignKey(limit_choices_to={'model__in': ('quiz', 'workshop')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='discountcode',
            name='object_id',
            field=gfklookupwidget.fields.GfkLookupField(),
        ),
    ]