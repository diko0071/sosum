from rest_framework import serializers
from .models import ScrapperLog

class ScrapperLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapperLog
        fields = (
            'scrap_date', 'scrapper_name', 'platform', 'scrapper_category', 'keyword', 'max_results', 'id'
        )