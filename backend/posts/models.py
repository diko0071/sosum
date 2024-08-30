from django.db import models
from platform_scrapper.models import ScrapperLog

class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    source_url = models.URLField(unique=True)
    date = models.DateField()

    scrapper_log = models.ForeignKey(ScrapperLog, on_delete=models.CASCADE)
    platform = models.CharField(max_length=255, blank=True)
    tags = models.CharField(max_length=255, blank=True)

    ai_summary = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.tags and self.scrapper_log:
            self.tags = self.scrapper_log.scrapper_category

        if not self.platform and self.scrapper_log:
            self.platform = self.scrapper_log.platform

        super().save(*args, **kwargs)

