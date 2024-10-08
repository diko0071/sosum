# Generated by Django 5.0.2 on 2024-09-05 22:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platform_scrapper', '0006_authorprofile'),
        ('posts', '0002_postsocial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postsocial',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='platform_scrapper.authorprofile'),
        ),
        migrations.CreateModel(
            name='PostSocialSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=2000)),
                ('related_posts', models.JSONField(blank=True, null=True)),
                ('post_source_date', models.DateField(blank=True, null=True)),
                ('platform', models.CharField(blank=True, choices=[('producthunt', 'Product Hunt'), ('bioarxiv', 'bioarxiv'), ('arxiv', 'arXiv'), ('twitter', 'Twitter'), ('linkedin', 'LinkedIn')], max_length=255, null=True)),
                ('posts_ai_summary', models.TextField(blank=True, null=True)),
                ('posts_ai_tags', models.CharField(blank=True, max_length=550, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='platform_scrapper.authorprofile')),
            ],
        ),
    ]
