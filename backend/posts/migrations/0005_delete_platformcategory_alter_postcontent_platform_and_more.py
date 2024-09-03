# Generated by Django 5.0.2 on 2024-09-03 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_platformcategory_category_slug_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PlatformCategory',
        ),
        migrations.AlterField(
            model_name='postcontent',
            name='platform',
            field=models.CharField(blank=True, choices=[('producthunt', 'Product Hunt'), ('bioarxiv', 'bioarxiv'), ('arxiv', 'arXiv'), ('twitter', 'Twitter'), ('linkedin', 'LinkedIn')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='postsocial',
            name='platform',
            field=models.CharField(blank=True, choices=[('producthunt', 'Product Hunt'), ('bioarxiv', 'bioarxiv'), ('arxiv', 'arXiv'), ('twitter', 'Twitter'), ('linkedin', 'LinkedIn')], max_length=255, null=True),
        ),
    ]
