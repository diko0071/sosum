import arxiv
from datetime import datetime, timedelta
import time
import requests
from bs4 import BeautifulSoup


class ArxivScraper:
    def __init__(self):
        self.search = arxiv.Search()
        self.search_query = []
        self.max_results = 10
        self.sort_by = arxiv.SortCriterion.Relevance
        self.sort_order = arxiv.SortOrder.Descending

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
        if sort_by == 'submittedDate':
            self.sort_by = arxiv.SortCriterion.SubmittedDate
        elif sort_by == 'relevance':
            self.sort_by = arxiv.SortCriterion.Relevance
        else:
            raise ValueError("sort_by must be either 'submittedDate' or 'relevance'")

        if sort_order == 'ascending':
            self.sort_order = arxiv.SortOrder.Ascending
        elif sort_order == 'descending':
            self.sort_order = arxiv.SortOrder.Descending
        else:
            raise ValueError("sort_order must be either 'ascending' or 'descending'")
        
    def get_all_categories(self):
        url = "https://arxiv.org/category_taxonomy"
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            categories = []
            taxonomy_list = soup.find('div', id='category_taxonomy_list')
            if not taxonomy_list:
                raise Exception("Category taxonomy list not found")

            for accordion_body in taxonomy_list.find_all('div', class_='accordion-body'):
                group_name = accordion_body.find_previous('h2', class_='accordion-head').text.strip()
                for column in accordion_body.find_all('div', class_='column'):
                    for category in column.find_all('div', class_='is-one-fifth'):
                        h4 = category.find('h4')
                        if h4:
                            code = h4.text.split()[0]
                            name = h4.find('span').text.strip() if h4.find('span') else h4.text.strip()
                            name = name.strip('()')
                            categories.append({
                                'slug': code,
                                'name': name
                            })
            
            if not categories:
                raise Exception("No categories found. The page structure might have changed.")
            
            return categories
        except requests.RequestException as e:
            raise Exception(f"Error fetching arXiv taxonomy: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error while parsing arXiv taxonomy: {str(e)}")

    def get_papers(self):
        query = ' AND '.join(self.search_query)
        self.search.query = query
        self.search.max_results = self.max_results
        self.search.sort_by = self.sort_by
        self.search.sort_order = self.sort_order

        papers = []
        for result in self.search.results():
            paper = {
                'title': result.title,
                'authors': [author.name for author in result.authors],
                'summary': result.summary,
                'published': result.published.strftime('%Y-%m-%d %H:%M:%S'),
                'link': result.entry_id,
                'primary_category': result.primary_category,
                'categories': result.categories,
                'cat': result.primary_category.split('.')[0] if result.primary_category else None
            }
            papers.append(paper)
        
        return papers