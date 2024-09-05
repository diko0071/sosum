from rest_framework import serializers
from .models import ScrapperLog, PlatformCategory, AuthorProfile

class ScrapperLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapperLog
        fields = (
            'scrap_date', 'scrapper_name', 'platform', 'scrapper_category', 'keyword', 'max_results', 'id'
        )


class PlatformCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformCategory
        fields = '__all__'


    def create(self, validated_data):
        existing_category = PlatformCategory.objects.filter(slug=validated_data['slug']).first()
        if existing_category:
            return existing_category
        return super().create(validated_data)
    
class AuthorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorProfile
        fields = ('name', 'username', 'profile_url', 'profile_avatar')

    def create(self, validated_data):
        username = validated_data.get('username')
        author, created = AuthorProfile.objects.update_or_create(
            username=username,
            defaults=validated_data
        )
        return author