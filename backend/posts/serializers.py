from rest_framework import serializers
from .models import PostContent, PromptLog, PostSocial, AuthorProfile, PostSocialSummary
from .services import openai_call
from .prompts import tag_post_prompt, summary_posts_prompt
from collections import Counter
import json
    
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
    scrapper_log_id = serializers.IntegerField(write_only=True, required=False)
    author = serializers.PrimaryKeyRelatedField(queryset=AuthorProfile.objects.all())

    class Meta:
        model = PostSocial
        fields = (
            'post_source_url', 'post_source_id', 'platform', 'scrapper_log_id', 'post_source_date', 
            'author', 'ai_tags', 'total_activity', 'title', 'description'
        )
        extra_kwargs = {
            'ai_tags': {'required': False},
            'total_activity': {'required': False},
        }

    def create(self, validated_data):
        existing_post = PostSocial.objects.filter(post_source_id=validated_data['post_source_id']).first()
        if existing_post:
            return existing_post
        
        content = f"Title: {validated_data.get('title', '')}\nDescription: {validated_data.get('description', '')}"
        system_message = tag_post_prompt
        tags = openai_call(system_message, content)
        validated_data['ai_tags'] = [tag.strip() for tag in tags.split(',')]

        instance = PostSocial.objects.create(**validated_data)

        return instance

class PromptLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptLog
        fields = (
            'system_message', 'user_message', 'response', 'cost', 'input_tokens', 'output_tokens'
        )

class PostSocialSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostSocialSummary
        fields = (
            'title', 'related_posts', 'author', 'post_source_date', 'platform', 'posts_ai_summary', 'posts_ai_tags'
        )

    def create(self, validated_data):
        related_posts = validated_data.get('related_posts')
        
        content = f"Posts for summary: {related_posts}"
        system_message = summary_posts_prompt
        summary = openai_call(system_message, content)
        validated_data['posts_ai_summary'] = summary

        all_tags = []
        for post in related_posts:
            tags = json.loads(post['tags'].replace("'", '"'))
            all_tags.extend(tags)

        tag_counter = Counter(all_tags)
        most_common_tags = [tag for tag, _ in tag_counter.most_common(3)]
        
        validated_data['posts_ai_tags'] = most_common_tags

        instance = PostSocialSummary.objects.create(**validated_data)

        return instance