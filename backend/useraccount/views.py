from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserDetailSerializer
from dj_rest_auth.views import UserDetailsView
from platform_scrapper.views import TwitterScrapper
from rest_framework import status


class CustomUserDetailsView(UserDetailsView):
    serializer_class = UserDetailSerializer

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_twitter_profile(request):
    scraper = TwitterScrapper()

    username = request.data.get('username')
    if not username:
        return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

    profile_info = scraper.get_user_info(username)
    
    formatted_profile = {
        "id": profile_info['id'],
        "name": profile_info['name'],
        "username": profile_info['username'],
        "platform": "Twitter",
        "profile_id": profile_info['id'],
        "profile_url": f"https://twitter.com/{profile_info['username']}",
        "avatar_url": profile_info['image'],
        "following_list": [
            {
                "profile_url": f"{username}",
                "platform": "Twitter"
            } for username in profile_info['following_list']
        ]
    }
    
    return Response(formatted_profile, status=status.HTTP_200_OK)