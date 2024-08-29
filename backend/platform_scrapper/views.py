from django.shortcuts import render
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
import os 
from .scrappers.arxiv_scrapper import ArxivScraper
from rest_framework.response import Response
from .scrappers.producthunt_scrapper import ProductHuntScraper
from datetime import datetime, timedelta

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

    papers = scraper.get_papers()

    return Response(papers, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_producthunt_posts(request):
    api_key = os.getenv('PRODUCTHUNT_DEVELOPER_TOKEN')
    if not api_key:
        return Response({"error": "API key not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    scraper = ProductHuntScraper(api_key)

    date_str = request.data.get('date')
    topic = request.data.get('topic')
    max_results = int(request.data.get('max_results', 50))

    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            scraper.filter_by_date(date)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    if topic:
        scraper.filter_by_topic(topic)

    products, error = scraper.get_products(max_results=max_results)

    if error:
        return Response({"error": error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if not products:
        return Response({"message": "No products found for the given criteria."}, status=status.HTTP_200_OK)

    return Response({"products": products}, status=status.HTTP_200_OK)