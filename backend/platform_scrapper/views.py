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
from .scrappers.hackernews_scrapper import HackerNewsScraper
from .models import ScrapperLog
from .serializers import ScrapperLogSerializer
from posts.serializers import PostContentSerializer
from .scrappers.twitter_scrapper import TwitterScrapper
import json
from dotenv import load_dotenv

load_dotenv()


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_arxiv_papers(request):
    scraper = ArxivScraper()

    date = request.data.get('date')
    category = request.data.get('category')
    keyword = request.data.get('keyword')
    max_results = request.data.get('max_results')

    if date:
        scraper.filter_by_date(date)
    if category:
        scraper.filter_by_category(category)
    if keyword:
        scraper.filter_by_keyword(keyword)
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
            "platform": "Arxiv",
            "tags": f'{keyword}, {category}' if keyword and category else keyword or category
        }
        formatted_papers.append(formatted_paper)

    log_data = {
        'scrap_date': datetime.now().date(),
        'scrapper_name': 'ArxivScraper',
        'platform': 'Arxiv',
        'scrapper_category': category or '',
        'keyword': keyword or '',
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

    return Response(formatted_paper, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_producthunt_posts(request):
    api_key = os.getenv('PRODUCTHUNT_DEVELOPER_TOKEN')
    if not api_key:
        return Response({"error": "API key not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    scraper = ProductHuntScraper(api_key)

    date_str = request.data.get('date')
    topic = request.data.get('category')
    max_results = int(request.data.get('max_results', 50))
    search_term = request.data.get('keyword')

    scraper.set_order("VOTES")

    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            scraper.filter_by_date(date)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    if topic:
        scraper.filter_by_topic(topic)

    if search_term:
        scraper.filter_by_search(search_term)

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
                        "platform": "Product Hunt",
                        "tags": ", ".join([topic["node"]["name"] for topic in product.get("topics", {}).get("edges", [])])
                    }
                    formatted_products.append(formatted_product)

    log_data = {
        'scrap_date': datetime.now().date(),
        'scrapper_name': 'ProductHuntScraper',
        'platform': 'Product Hunt',
        'scrapper_category': topic or '',
        'keyword': search_term or '',
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

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_hackernews_posts(request):
    scraper = HackerNewsScraper()

    date_str = request.data.get('date')
    max_results = request.data.get('max_results')
    post_type = request.data.get('post_type', 'posts')
    keyword = request.data.get('keyword')

    if date_str:
        try:
            scraper.filter_by_date(date_str)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    if max_results:
        max_results = int(max_results)
    else:
        max_results = 50

    if post_type == 'asks':
        posts = scraper.get_asks(max_results=max_results)
    else:
        posts = scraper.get_posts(max_results=max_results)

    if keyword:
        posts = scraper.filter_by_keyword(posts, keyword)

    posts = scraper.set_order(posts, order_by='score', reverse=True)

    if not posts:
        return Response({"message": "No posts found for the given criteria."}, status=status.HTTP_200_OK)

    formatted_posts = []
    for post in posts:
        post_id = post.get("id", "")
        formatted_post = {
            "title": post.get("title", ""),
            "description": post.get("text", ""),
            "post_source_url": f"https://news.ycombinator.com/item?id={post_id}",
            "post_source_id": post_id,
            "post_source_date": datetime.fromtimestamp(post.get("time", 0)).strftime('%Y-%m-%d'),
            "platform": "Hacker News",
            "tags": ""
        }
        formatted_posts.append(formatted_post)

    log_data = {
        'scrap_date': datetime.now().date(),
        'scrapper_name': 'HackerNewsScraper',
        'platform': 'Hacker News',
        'scrapper_category': "",
        'keyword': keyword or '',
        'max_results': max_results,
    }
    
    serializer = ScrapperLogSerializer(data=log_data)
    
    if serializer.is_valid():
        scrapper_log = serializer.save()

        for formatted_post in formatted_posts:
            formatted_post['scrapper_log_id'] = scrapper_log.id
            post_serializer = PostContentSerializer(data=formatted_post)
            if post_serializer.is_valid():
                post_serializer.save()
            else:
                return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(formatted_posts, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_twitter_posts(request):
    scraper = TwitterScrapper()

    username = request.data.get('username')
    if not username:
        return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

    since_str = request.data.get('since')
    until_str = request.data.get('until')
    max_results = int(request.data.get('max_results', 50))

    since = datetime.strptime(since_str, '%Y-%m-%d') if since_str else None
    until = datetime.strptime(until_str, '%Y-%m-%d') if until_str else None

    tweets_data = scraper.get_tweets(username, since=since, until=until, number=max_results)
    
    if isinstance(tweets_data, str):
        try:
            tweets_data = json.loads(tweets_data)
        except json.JSONDecodeError:
            return Response({"error": "Invalid data format from Twitter scraper"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    tweets = tweets_data.get('tweets', [])

    if not tweets:
        return Response({"message": "No tweets found for the given criteria."}, status=status.HTTP_200_OK)

    formatted_tweets = []
    
    for tweet in tweets:
        post_source_id = tweet['link'].split('/')[-1].split('#')[0]
        
        date_str = tweet['date']
        date_obj = datetime.strptime(date_str, "%b %d, %Y · %I:%M %p UTC")
        formatted_date = date_obj.strftime("%Y-%m-%d")

        formatted_tweet = {
            "post_source_url": tweet['link'],
            "post_source_id": post_source_id,
            "title": tweet['text'],
            "post_source_date": formatted_date,
            "platform": "Twitter",
            "author": {
                "name": tweet['user']['name'],
                "username": tweet['user']['username'],
                "profile_url": f"https://twitter.com/{tweet['user']['username'].lstrip('@')}",
                "profile_avatar": tweet['user']['avatar']
            }
        }
        formatted_tweets.append(formatted_tweet)

    return Response(formatted_tweets, status=status.HTTP_200_OK)