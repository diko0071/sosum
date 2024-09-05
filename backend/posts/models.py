from django.db import models
from platform_scrapper.models import ScrapperLog
from datetime import datetime
from django.contrib.auth.models import User
from platform_scrapper.models import PlatformName, AuthorProfile

class PostContent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    post_source_url = models.URLField(max_length=2000, blank=True, null=True)
    post_source_id = models.CharField(max_length=2000, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    post_source_date = models.DateField(blank=True, null=True)
    platform = models.CharField(max_length=255, choices=PlatformName.choices, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)

    scrapper_log = models.ForeignKey(ScrapperLog, on_delete=models.CASCADE, blank=True, null=True)

    ai_summary = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PostSocial(models.Model):
    title = models.CharField(max_length=2000)
    description = models.TextField(null=True, blank=True)
    post_source_url = models.URLField(max_length=2000, blank=True, null=True)
    post_source_id = models.CharField(max_length=2000, blank=True, null=True)
    post_source_date = models.DateField(blank=True, null=True)
    platform = models.CharField(max_length=255, choices=PlatformName.choices, blank=True, null=True)
    total_activity = models.PositiveIntegerField(blank=True, null=True)
    
    author = models.ForeignKey(AuthorProfile, on_delete=models.CASCADE, blank=True, null=True)

    scrapper_log = models.ForeignKey(ScrapperLog, on_delete=models.CASCADE, blank=True, null=True)

    ai_tags = models.CharField(max_length=255, blank=True, null=True)
    ai_summary = models.TextField(blank=True, null=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class PostSocialSummary(models.Model):
    title = models.CharField(max_length=2000)
    related_posts = models.JSONField(blank=True, null=True)

    author = models.ForeignKey(AuthorProfile, on_delete=models.CASCADE, blank=True, null=True)
    
    post_source_date = models.DateField(blank=True, null=True)
    platform = models.CharField(max_length=255, choices=PlatformName.choices, blank=True, null=True)

    posts_ai_summary = models.TextField(blank=True, null=True)
    posts_ai_tags = models.CharField(max_length=550, blank=True, null=True)

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