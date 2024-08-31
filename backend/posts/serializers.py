from rest_framework import serializers
from .models import PostContent, PostSocial
    
class PostContentSerializer(serializers.ModelSerializer):
    scrapper_log_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = PostContent
        fields = (
            'title', 'description', 'post_source_url', 'post_source_id', 'author', 'ai_summary', 'platform', 'tags', 'scrapper_log_id', 'post_source_date'
        )