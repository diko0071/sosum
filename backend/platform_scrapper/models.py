from django.db import models


class ScrapperLog(models.Model):
    date = models.DateField()
    scrapper_name = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    scrapper_category = models.CharField(max_length=255)
    keyword = models.CharField(max_length=255)
    max_results = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    