# Generated by Django 5.0.2 on 2024-09-05 23:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platform_scrapper', '0008_alter_authorprofile_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scrapperlog',
            name='keyword',
        ),
        migrations.RemoveField(
            model_name='scrapperlog',
            name='max_results',
        ),
        migrations.RemoveField(
            model_name='scrapperlog',
            name='scrapper_category',
        ),
    ]
