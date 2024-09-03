from django.db import models

class PlatformName(models.TextChoices):
    PRODUCTHUNT = 'producthunt', 'Product Hunt'
    BIOARXIV = 'bioarxiv', 'bioarxiv'
    ARXIV = 'arxiv', 'arXiv'
    TWITTER = 'twitter', 'Twitter'
    LINKEDIN = 'linkedin', 'LinkedIn'


class PlatformCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, blank=True, null=True)
    platform = models.CharField(max_length=255, choices=PlatformName.choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ScrapperLog(models.Model):
    scrap_date = models.DateField()
    scrapper_name = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    scrapper_category = models.CharField(max_length=255, blank=True)
    keyword = models.CharField(max_length=255, blank=True)
    max_results = models.IntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)