from rest_framework import serializers
from .models import PostContent, PostSocial, PromptLog
    
class PostContentSerializer(serializers.ModelSerializer):
    scrapper_log_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = PostContent
        fields = (
            'title', 'description', 'post_source_url', 'post_source_id', 'author', 'ai_summary', 'platform', 'tags', 'scrapper_log_id', 'post_source_date'
        )
    
    def create(self, validated_data):
        existing_post = PostContent.objects.filter(post_source_id=validated_data['post_source_id']).first()
        if existing_post:
            return existing_post
        return super().create(validated_data)
    
class PostSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostSocial
        fields = (
            'post_source_url', 'post_source_id', 'platform', 'tags', 'scrapper_log_id', 'post_source_date', 'author'
        )

    def create(self, validated_data):
        existing_post = PostSocial.objects.filter(post_source_id=validated_data['post_source_id']).first()
        if existing_post:
            return existing_post
        return super().create(validated_data)

class PromptLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptLog
        fields = (
            'system_message', 'user_message', 'response', 'cost', 'input_tokens', 'output_tokens'
        )
