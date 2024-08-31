from django.urls import path
from .views import *

urlpatterns = [
    path('arxiv/get_list/', get_arxiv_papers, name='arxiv_papers'),
    path('producthunt/get_list/', get_producthunt_posts, name='producthunt_posts'),
    path('hackernews/get_list/', get_hackernews_posts, name='hackernews_posts'),
    path('twitter/get_list/', get_twitter_posts, name='twitter_posts')
]