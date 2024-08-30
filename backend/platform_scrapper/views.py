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
            "url": paper.get("link", ""),
            "id": paper.get("link", "").split("/")[-1],
            "category": paper.get("primary_category", ""),
            "date": paper.get("published", "")[:10] 
        }
        formatted_papers.append(formatted_paper)

    return Response(formatted_papers, status=status.HTTP_200_OK)

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
                        "url": product.get("url", ""), 
                        "id": product.get("id", ""), 
                        "category": ", ".join([topic["node"]["name"] for topic in product.get("topics", {}).get("edges", [])]),
                        "date": product.get("createdAt", "")[:10]
                    }
                    formatted_products.append(formatted_product)

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
            "url": f"https://news.ycombinator.com/item?id={post_id}",
            "id": post_id,
            "category": "",
            "date": datetime.fromtimestamp(post.get("time", 0)).strftime('%Y-%m-%d')
        }
        formatted_posts.append(formatted_post)

    return Response(formatted_posts, status=status.HTTP_200_OK)

