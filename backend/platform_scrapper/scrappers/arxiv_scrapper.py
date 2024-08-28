import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

class ArxivScraper:
    def __init__(self):
        self.base_url = 'http://export.arxiv.org/api/query?'
        self.params = {
            'search_query': '',
            'start': 0,
            'max_results': 10
        }

    def filter_by_category(self, category):
        self.params['search_query'] += f'cat:{category}'

    def filter_by_date(self, date):
        self.params['search_query'] += f' AND submittedDate:[{date} TO *]'

    def filter_by_keyword(self, keyword):
        self.params['search_query'] += f' AND all:{keyword}'

    def set_max_results(self, max_results):
        self.params['max_results'] = max_results

    def get_papers(self):
        query_string = urllib.parse.urlencode(self.params)
        url = self.base_url + query_string
        
        with urllib.request.urlopen(url) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        
        papers = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            paper = {
                'title': entry.find('{http://www.w3.org/2005/Atom}title').text,
                'authors': [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')],
                'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text,
                'published': entry.find('{http://www.w3.org/2005/Atom}published').text,
                'link': entry.find('{http://www.w3.org/2005/Atom}id').text
            }
            papers.append(paper)
        
        return papers