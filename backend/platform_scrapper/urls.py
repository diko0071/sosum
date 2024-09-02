from django.urls import path
from .views import *

urlpatterns = [
    path('arxiv/get_list/', scrap_arxiv_papers, name='arxiv_papers'),
    path('producthunt/get_list/', scrap_producthunt_posts, name='producthunt_posts'),
    path('twitter/get_list/', scrap_twitter_posts, name='twitter_posts'),
    path('linkedin/get_list/', scrap_linkedin_posts, name='linkedin_posts'),
    path('bioarxiv/get_list/', scrap_bioarxiv_papers, name='bioarxiv_papers'),
    path('producthunt/get_categories/', scrap_producthunt_categories, name='producthunt_categories'),
    path('bioarxiv/get_categories/', scrap_bioarxiv_categories, name='bioarxiv_categories'),
    path('arxiv/get_categories/', scrap_arxiv_categories, name='arxiv_categories'),
]