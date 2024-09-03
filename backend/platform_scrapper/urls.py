from django.urls import path
from .views import *

urlpatterns = [
    path('arxiv/scrap_list/', scrap_arxiv_papers, name='arxiv_papers'),
    path('producthunt/scrap_list/', scrap_producthunt_posts, name='producthunt_posts'),
    path('twitter/scrap_list/', scrap_twitter_posts, name='twitter_posts'),
    path('linkedin/scrap_list/', scrap_linkedin_posts, name='linkedin_posts'),
    path('bioarxiv/scrap_list/', scrap_bioarxiv_papers, name='bioarxiv_papers'),
    path('producthunt/scrap_categories/', scrap_producthunt_categories, name='producthunt_categories'),
    path('bioarxiv/scrap_categories/', scrap_bioarxiv_categories, name='bioarxiv_categories'),
    path('arxiv/scrap_categories/', scrap_arxiv_categories, name='arxiv_categories'),
]