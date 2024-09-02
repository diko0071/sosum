from django.urls import path
from .views import *

urlpatterns = [
    path('arxiv/get_list/', get_arxiv_papers, name='arxiv_papers'),
    path('producthunt/get_list/', get_producthunt_posts, name='producthunt_posts'),
    path('hackernews/get_list/', get_hackernews_posts, name='hackernews_posts'),
    path('twitter/get_list/', get_twitter_posts, name='twitter_posts'),
    path('linkedin/get_list/', get_linkedin_posts, name='linkedin_posts'),
    path('bioarxiv/get_list/', get_bioarxiv_papers, name='bioarxiv_papers'),
]