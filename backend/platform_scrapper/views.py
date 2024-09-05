from django.shortcuts import render
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
import os 
from .scrappers.arxiv_scrapper import ArxivScraper
from rest_framework.response import Response
from .scrappers.producthunt_scrapper import ProductHuntScraper
from datetime import datetime
from .models import ScrapperLog
from .serializers import ScrapperLogSerializer, PlatformCategorySerializer, AuthorProfileSerializer
from posts.serializers import PostContentSerializer, PostSocialSerializer
from .scrappers.twitter_scrapper import TwitterScrapper
import json
from dotenv import load_dotenv
from .scrappers.linkedin_scrapper import LinkedinScrapper
from .services import convert_linkedin_relative_datetime_to_date
from .scrappers.bioarxiv_scrapper import BioarxivScraper


load_dotenv()


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def scrap_arxiv_papers(request):
    scraper = ArxivScraper()

    date = request.data.get('date')
    category = request.data.get('category')
    max_results = request.data.get('max_results')

    if date:
        scraper.filter_by_date(date)
    if category:
        scraper.filter_by_category(category)
    if max_results:
        scraper.set_max_results(int(max_results))

    scraper.set_order('submittedDate', "descending")

    papers = scraper.get_papers()

    formatted_papers = []
    for paper in papers:
        formatted_paper = {
            "title": paper.get("title", "").replace("\n", " ").strip(),
            "description": paper.get("summary", "").replace("\n", " ").strip(),
            "post_source_url": paper.get("link", ""),
            "post_source_id": paper.get("link", "").split("/")[-1],
            "post_source_date": paper.get("published", "")[:10],
            "platform": "arxiv",
            "tags": paper.get("cat", "")
        }
        formatted_papers.append(formatted_paper)

    log_data = {
        'scrap_date': datetime.now().date(),
        'scrapper_name': 'ArxivScraper',
        'platform': 'arxiv',
        'scrapper_category': category or '',
        'keyword': '',
        'max_results': max_results or 0,
    }

    serializer = ScrapperLogSerializer(data=log_data)
    
    if serializer.is_valid():
        scrapper_log = serializer.save()

        for formatted_paper in formatted_papers:
            formatted_paper['scrapper_log_id'] = scrapper_log.id
            post_serializer = PostContentSerializer(data=formatted_paper)
            if post_serializer.is_valid():
                post_serializer.save()
            else:
                return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(formatted_papers, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def scrap_producthunt_posts(request):
    api_key = os.getenv('PRODUCTHUNT_DEVELOPER_TOKEN')
    if not api_key:
        return Response({"error": "API key not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    scraper = ProductHuntScraper(api_key)

    date_str = request.data.get('date')
    topic = request.data.get('category')
    max_results = int(request.data.get('max_results', 50))

    scraper.set_order("VOTES")

    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            scraper.filter_by_date(date)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    if topic:
        scraper.filter_by_topic(topic)

    products = scraper.get_products(max_results=max_results)

    if not products:
        return Response({"message": "No products found for the given criteria."}, status=status.HTTP_200_OK)

    formatted_products = []
    for product_list in products:
        if isinstance(product_list, list):
            for product in product_list:
                if isinstance(product, dict):
                    formatted_product = {
                        "title": product.get("name", ""), 
                        "description": product.get("description", ""), 
                        "post_source_url": product.get("url", ""), 
                        "post_source_id": product.get("id", ""), 
                        "post_source_date": product.get("createdAt", "")[:10],
                        "platform": "producthunt",
                        "tags": ", ".join([topic["node"]["name"] for topic in product.get("topics", {}).get("edges", [])])
                    }
                    formatted_products.append(formatted_product)

    log_data = {
        'scrap_date': datetime.now().date(),
        'scrapper_name': 'ProductHuntScraper',
        'platform': 'producthunt',
        'scrapper_category': '',
        'keyword':  '',
        'max_results': max_results,
    }
    
    serializer = ScrapperLogSerializer(data=log_data)
    
    if serializer.is_valid():
        scrapper_log = serializer.save()

        for formatted_product in formatted_products:
            formatted_product['scrapper_log_id'] = scrapper_log.id
            post_serializer = PostContentSerializer(data=formatted_product)
            if post_serializer.is_valid():
                post_serializer.save()
            else:
                return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(formatted_products, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def scrap_twitter_posts(request):
    nitter_instances_str = os.getenv('NITTER_INSTANCES')
    if not nitter_instances_str:
        return Response({"error": "NITTER_INSTANCES not configured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    NITTER_INSTANCES = nitter_instances_str.split(',')
    
    username = request.data.get('username')
    if not username:
        return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

    since_str = request.data.get('date')
    max_results = int(request.data.get('max_results', 50))

    since = datetime.strptime(since_str, '%Y-%m-%d') if since_str else None

    tweets = []
    for instance in NITTER_INSTANCES:
        scraper = TwitterScrapper(instance=instance)
        tweets_data = scraper.get_tweets(username, since=since, number=max_results)
        
        if isinstance(tweets_data, str):
            try:
                tweets_data = json.loads(tweets_data)
            except json.JSONDecodeError:
                continue 

        tweets = tweets_data.get('tweets', [])
        if tweets:
            break

    if not tweets:
        return Response({"message": "No tweets found for the given criteria across all instances."}, status=status.HTTP_200_OK)

    formatted_tweets = []
    
    for tweet in tweets:
        post_source_id = tweet['link'].split('/')[-1].split('#')[0]
        
        date_str = tweet['date']
        date_obj = datetime.strptime(date_str, "%b %d, %Y · %I:%M %p UTC")
        formatted_date = date_obj.strftime("%Y-%m-%d")

        stats = tweet['stats']
        total_activity = sum(stats.values())


        author_data = {
            "name": tweet['user']['name'],
            "username": tweet['user']['username'],
            "profile_url": f"https://twitter.com/{tweet['user']['username'].lstrip('@')}",
            "profile_avatar": tweet['user']['avatar'],
            "platform": "twitter"
        }
        author_serializer = AuthorProfileSerializer(data=author_data)

        if author_serializer.is_valid():
            author = author_serializer.save()
        else:
            return Response(author_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        formatted_tweet = {
            "post_source_url": tweet['link'],
            "post_source_id": post_source_id,
            "title": f"{tweet['user']['name']} Tweet",
            "description": tweet['text'],
            "post_source_date": formatted_date,
            "platform": "twitter",
            "total_activity": total_activity,
            "ai_tags": "",
            "author": author.id
        }
        formatted_tweets.append(formatted_tweet)

    log_data = {
        'scrap_date': datetime.now().date(),
        'scrapper_name': 'TwitterScraper',
        'platform': 'twitter',
        'scrapper_category': '',
        'keyword': '',
        'max_results': max_results,
    }

    log_serializer = ScrapperLogSerializer(data=log_data)
    
    if log_serializer.is_valid():
        scrapper_log = log_serializer.save()

        for formatted_tweet in formatted_tweets:
            formatted_tweet['scrapper_log_id'] = scrapper_log.id
            post_serializer = PostSocialSerializer(data=formatted_tweet)
            if post_serializer.is_valid():
                post_serializer.save()
            else:
                return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(formatted_tweets, status=status.HTTP_200_OK)



@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def scrap_linkedin_posts(request):
    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')
    scraper = LinkedinScrapper(email, password)

    username = request.data.get('username')
    date_str = request.data.get('date')

    if not username:
        return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

    max_results = int(request.data.get('max_results', 50))
    
    posts = scraper.get_profile_posts(username, max_results)

    if date_str:
        try:
            requested_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        requested_date = None
    
    if not posts:
        return Response({"message": "No posts found for the given criteria."}, status=status.HTTP_200_OK)

    formatted_posts = []
    for post in posts:
        relative_time_str = post.get('actor', {}).get('subDescription', {}).get('text', '')
        post_date = convert_linkedin_relative_datetime_to_date(relative_time_str.split('•')[0].strip())

        if post_date is None:
            continue
        
        if requested_date and post_date != requested_date.strftime('%Y-%m-%d'):
            continue

        post_activity = post.get('socialDetail', {}).get('totalSocialActivityCounts', {})
        total_reactions = sum(reaction.get('count', 0) for reaction in post_activity.get('reactionTypeCounts', []))
        num_comments = post_activity.get('numComments', 0)
        combined_activity = total_reactions + num_comments

        mini_profile = post.get('actor', {}).get('image', {}).get('attributes', [{}])[0].get('miniProfile', {})
        author_name = mini_profile.get('firstName', '') + ' ' + mini_profile.get('lastName', '')
        author_username = mini_profile.get('publicIdentifier', '')
        author_profile_url = f"https://www.linkedin.com/in/{author_username}"
        author_profile_avatar = mini_profile.get('picture', {}).get('com.linkedin.common.VectorImage', {}).get('rootUrl', '') + \
                                mini_profile.get('picture', {}).get('com.linkedin.common.VectorImage', {}).get('artifacts', [{}])[-1].get('fileIdentifyingUrlPathSegment', '')

        author_data = {
            "name": author_name,
            "username": author_username,
            "profile_url": author_profile_url,
            "profile_avatar": author_profile_avatar,
            "platform": "linkedin"
        }
        author_serializer = AuthorProfileSerializer(data=author_data)

        if author_serializer.is_valid():
            author = author_serializer.save()
        else:
            return Response(author_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        formatted_post = {
            "post_source_url": post.get('socialContent', {}).get('shareUrl', ''),
            "post_source_id": post.get('updateMetadata', {}).get('urn', ''),
            "title": f"{author_name} Post",
            "description": post.get('commentary', {}).get('text', {}).get('text', ''), 
            "post_source_date": post_date,
            "platform": "linkedin",
            "total_activity": combined_activity,
            "ai_tags": "",
            "author": author.id
        }
        formatted_posts.append(formatted_post)

    log_data = {
        'scrap_date': datetime.now().date(),
        'scrapper_name': 'LinkedinScraper',
        'platform': 'linkedin',
        'scrapper_category': '',
        'keyword': '',
        'max_results': max_results,
    }

    log_serializer = ScrapperLogSerializer(data=log_data)
    
    if log_serializer.is_valid():
        scrapper_log = log_serializer.save()

        for formatted_post in formatted_posts:
            formatted_post['scrapper_log_id'] = scrapper_log.id
            post_serializer = PostSocialSerializer(data=formatted_post)
            if post_serializer.is_valid():
                post_serializer.save()
            else:
                return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(formatted_posts, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def scrap_bioarxiv_papers(request):
    scraper = BioarxivScraper()

    date = request.data.get('date')
    category = request.data.get('category')
    max_results = request.data.get('max_results', 100)

    start_date = date
    end_date = date

    if start_date:
        scraper.filter_by_date_range(start_date, end_date)
    elif date:
        scraper.filter_by_recent_days(int(date))
    elif max_results:
        scraper.filter_by_most_recent(int(max_results))
    else:
        scraper.filter_by_most_recent(100)

    papers = scraper.get_papers()

    if category:
        papers = [paper for paper in papers if category.lower() in paper['category'].lower()]

    if max_results:
        papers = papers[:int(max_results)]

    formatted_papers = []
    for paper in papers:
        formatted_paper = {
            "title": paper['title'].replace("\n", " ").strip(),
            "description": paper['abstract'].replace("\n", " ").strip(),
            "post_source_url": f"https://www.biorxiv.org/content/{paper['doi']}v{paper['version']}",
            "post_source_id": paper['doi'],
            "post_source_date": paper['date'],
            "platform": "bioarxiv",
            "tags": paper['category'] or ""
        }
        formatted_papers.append(formatted_paper)

    log_data = {
        'scrap_date': datetime.now().date(),
        'scrapper_name': 'BioarxivScraper',
        'platform': 'bioarxiv',
        'scrapper_category': '',
        'keyword': '',
        'max_results': max_results
    }

    serializer = ScrapperLogSerializer(data=log_data)
    
    if serializer.is_valid():
        scrapper_log = serializer.save()

        for formatted_paper in formatted_papers:
            formatted_paper['scrapper_log_id'] = scrapper_log.id
            post_serializer = PostContentSerializer(data=formatted_paper)
            if post_serializer.is_valid():
                post_serializer.save()
            else:
                return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(papers, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def scrap_producthunt_categories(request):
    api_key = os.getenv('PRODUCTHUNT_DEVELOPER_TOKEN')
    if not api_key:
        return Response({"error": "API key not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    scraper = ProductHuntScraper(api_key)
    categories = scraper.get_all_topics()
    
    saved_categories = []
    for category in categories:
        serializer = PlatformCategorySerializer(data={
            'slug': category['slug'],
            'name': category['name'],
            'platform': 'producthunt'
        })
        if serializer.is_valid():
            serializer.save()
            saved_categories.append(serializer.data)
    
    return Response(saved_categories, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def scrap_bioarxiv_categories(request):
    scraper = BioarxivScraper()
    categories = scraper.get_all_categories()
    
    saved_categories = []
    for category in categories:
        serializer = PlatformCategorySerializer(data={
            'slug': category['slug'],
            'name': category['name'],
            'platform': 'bioarxiv'
        })
        if serializer.is_valid():
            serializer.save()
            saved_categories.append(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(saved_categories, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def scrap_arxiv_categories(request):
    scraper = ArxivScraper()
    categories = scraper.get_all_categories()
    
    saved_categories = []
    for category in categories:
        serializer = PlatformCategorySerializer(data={
            'slug': category['slug'],
            'name': category['name'],
            'platform': 'arxiv'
        })
        if serializer.is_valid():
            serializer.save()
            saved_categories.append(serializer.data)
    
    return Response(saved_categories, status=status.HTTP_200_OK)