# Generated by Django 5.0.2 on 2024-09-05 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platform_scrapper', '0006_authorprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='authorprofile',
            name='platform',
            field=models.CharField(blank=True, choices=[('producthunt', 'Product Hunt'), ('bioarxiv', 'bioarxiv'), ('arxiv', 'arXiv'), ('twitter', 'Twitter'), ('linkedin', 'LinkedIn')], max_length=255, null=True),
        ),
    ]
