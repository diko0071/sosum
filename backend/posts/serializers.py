from rest_framework import serializers
from .models import PostContent, PostSocial, PromptLog
    
class PostContentSerializer(serializers.ModelSerializer):
    scrapper_log_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = PostContent
        fields = (
            'title', 'description', 'post_source_url', 'post_source_id', 'author', 'ai_summary', 'platform', 'tags', 'scrapper_log_id', 'post_source_date'
        )

class PostSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostSocial
        fields = (
            'post_id', 'post_source_url', 'post_source_id', 'platform', 'tags', 'scrapper_log_id', 'post_source_date', 'author'
        )

class PromptLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptLog
        fields = (
            'system_message', 'user_message', 'response', 'cost', 'input_tokens', 'output_tokens'
        )
