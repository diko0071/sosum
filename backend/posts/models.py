from django.db import models
from platform_scrapper.models import ScrapperLog
from datetime import datetime

class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    post_source_url = models.URLField(unique=False, blank=True, null=True)
    post_source_id = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    post_source_date = models.DateField(blank=True, null=True)
    platform = models.CharField(max_length=255, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)

    scrapper_log = models.ForeignKey(ScrapperLog, on_delete=models.CASCADE, blank=True, null=True)
    

    ai_summary = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
