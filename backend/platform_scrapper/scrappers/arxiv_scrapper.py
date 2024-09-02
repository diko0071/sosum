import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

class ArxivScraper:
    def __init__(self):
        self.base_url = 'http://export.arxiv.org/api/query?'
        self.search_query = []
        self.max_results = 10

    def filter_by_category(self, category):
        self.search_query.append(f'cat:{category}')

    def filter_by_date(self, date):
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d")
            next_day = parsed_date + timedelta(days=1)
            formatted_date = next_day.strftime("%Y%m%d%H%M%S")
            self.search_query.append(f'submittedDate:[* TO {formatted_date}]')
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

    def filter_by_keyword(self, keyword):
        self.search_query.append(f'all:{keyword}')

    def set_max_results(self, max_results):
        self.max_results = max_results

    def set_order(self, sort_by, sort_order='descending'):
        if sort_by not in ['submittedDate', 'relevance']:
            raise ValueError("sort_by must be either 'submittedDate' or 'relevance'")
        if sort_order not in ['ascending', 'descending']:
            raise ValueError("sort_order must be either 'ascending' or 'descending'")
        
        self.sort_by = sort_by
        self.sort_order = sort_order

    def get_all_categories(self):
        url = 'http://export.arxiv.org/oai2?verb=ListSets'
        
        with urllib.request.urlopen(url) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        categories = []
        for set_elem in root.findall('.//{http://www.openarchives.org/OAI/2.0/}set'):
            spec = set_elem.find('{http://www.openarchives.org/OAI/2.0/}setSpec').text
            name = set_elem.find('{http://www.openarchives.org/OAI/2.0/}setName').text
            categories.append({'spec': spec, 'name': name})
        
        return categories

    def get_papers(self):
        params = {
            'search_query': ' AND '.join(self.search_query),
            'start': 0,
            'max_results': self.max_results,
            'sortBy': self.sort_by,
            'sortOrder': self.sort_order
        }
        query_string = urllib.parse.urlencode(params)
        url = self.base_url + query_string
        
        with urllib.request.urlopen(url) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        
        papers = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            primary_category = entry.find('{http://arxiv.org/schemas/atom}primary_category')
            categories = entry.findall('{http://www.w3.org/2005/Atom}category')

            paper = {
                'title': entry.find('{http://www.w3.org/2005/Atom}title').text,
                'authors': [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')],
                'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text,
                'published': entry.find('{http://www.w3.org/2005/Atom}published').text,
                'link': entry.find('{http://www.w3.org/2005/Atom}id').text,
                'primary_category': primary_category.get('term') if primary_category is not None else None,
                'categories': [category.get('term') for category in categories],
                'cat': primary_category.get('term').split('.')[0] if primary_category is not None else None
            }
            papers.append(paper)
        
        return papers