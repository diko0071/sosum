import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class BioarxivScraper:
    def __init__(self):
        self.base_url = 'https://api.biorxiv.org/details/biorxiv/'
        self.start_date = None
        self.end_date = None
        self.max_results = 100
        self.cursor = 0

    def filter_by_date_range(self, start_date, end_date):
        try:
            self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
            self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

    def filter_by_recent_days(self, days):
        self.end_date = datetime.now()
        self.start_date = self.end_date - timedelta(days=days)

    def filter_by_most_recent(self, count):
        self.max_results = count

    def set_cursor(self, cursor):
        self.cursor = cursor

    def get_all_categories(self):
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        url = f"{self.base_url}{start_date}/{end_date}/0"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            all_categories = [item['category'] for item in data.get('collection', [])]
            unique_categories = sorted(set(all_categories))
            
            def capitalize_name(name):
                words = name.split()
                capitalized_words = [word.capitalize() if word.lower() not in ['of', 'and', 'or'] else word.lower() for word in words]
                return ' '.join(capitalized_words)
            
            formatted_categories = [
                {
                    "slug": category.strip(),
                    "name": capitalize_name(category.strip())
                }
                for category in unique_categories
            ]
            
            return formatted_categories
        else:
            print(f"Error fetching data: {response.status_code}")
            return []

    def get_papers(self):
        if self.start_date and self.end_date:
            date_param = f"{self.start_date.strftime('%Y-%m-%d')}/{self.end_date.strftime('%Y-%m-%d')}"
        elif self.max_results:
            date_param = str(self.max_results)
        else:
            raise ValueError("Please set either a date range or the number of most recent papers.")

        url = f"{self.base_url}{date_param}/{self.cursor}/json"
        
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")

        data = response.json()
        papers = data.get('collection', [])

        processed_papers = []
        for paper in papers:
            processed_paper = {
                'doi': paper.get('doi'),
                'title': paper.get('title'),
                'authors': paper.get('authors'),
                'author_corresponding': paper.get('author_corresponding'),
                'author_corresponding_institution': paper.get('author_corresponding_institution'),
                'date': paper.get('date'),
                'version': paper.get('version'),
                'category': paper.get('category'),
                'abstract': paper.get('abstract'),
                'published': paper.get('published'),
                'server': 'bioRxiv'
            }
            processed_papers.append(processed_paper)

        return processed_papers

    def get_paper_by_doi(self, doi):
        url = f"{self.base_url}{doi}/na/json"
        
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")

        data = response.json()
        paper = data.get('collection', [])
        
        if paper:
            return {
                'doi': paper[0].get('doi'),
                'title': paper[0].get('title'),
                'authors': paper[0].get('authors'),
                'author_corresponding': paper[0].get('author_corresponding'),
                'author_corresponding_institution': paper[0].get('author_corresponding_institution'),
                'date': paper[0].get('date'),
                'version': paper[0].get('version'),
                'category': paper[0].get('category'),
                'abstract': paper[0].get('abstract'),
                'published': paper[0].get('published'),
                'server': 'bioRxiv'
            }
        else:
            return None