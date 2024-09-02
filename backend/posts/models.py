from django.db import models
from platform_scrapper.models import ScrapperLog
from datetime import datetime
from django.contrib.auth.models import User


class Platforms(models.TextChoices):
    PRODUCTHUNT = 'producthunt', 'Product Hunt'
    BIOARXIV = 'bioarxiv', 'bioarxiv'
    ARXIV = 'arxiv', 'arXiv'
    TWITTER = 'twitter', 'Twitter'
    LINKEDIN = 'linkedin', 'LinkedIn'
    HACKERNEWS = 'hackernews', 'Hacker News'
class PostContent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    post_source_url = models.URLField(unique=False, blank=True, null=True)
    post_source_id = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    post_source_date = models.DateField(blank=True, null=True)
    platform = models.CharField(max_length=255, choices=Platforms.choices, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)

    scrapper_log = models.ForeignKey(ScrapperLog, on_delete=models.CASCADE, blank=True, null=True)

    ai_summary = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PostSocial(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    post_source_url = models.URLField(unique=False, blank=True, null=True)
    post_source_id = models.CharField(max_length=255, blank=True, null=True)
    post_source_date = models.DateField(blank=True, null=True)
    platform = models.CharField(max_length=255, choices=Platforms.choices, blank=True, null=True)
    total_activity = models.PositiveIntegerField(blank=True, null=True)

    author = models.JSONField(blank=True, null=True)

    scrapper_log = models.ForeignKey(ScrapperLog, on_delete=models.CASCADE, blank=True, null=True)

    ai_tag = models.CharField(max_length=255, blank=True, null=True)
    ai_summary = models.TextField(blank=True, null=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class PromptLog(models.Model):
    system_message = models.TextField()
    user_message = models.TextField()
    response = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=10)
    input_tokens = models.PositiveIntegerField(null=True, blank=True)
    output_tokens = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

class PlatformCategory(models.Model):
    category_name = models.CharField(max_length=255)
    category_slug = models.CharField(max_length=255, blank=True, null=True)
    platform = models.CharField(max_length=255, choices=Platforms.choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)