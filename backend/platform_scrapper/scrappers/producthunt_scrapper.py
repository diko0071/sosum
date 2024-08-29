import requests
from datetime import datetime, timedelta

class ProductHuntScraper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = 'https://api.producthunt.com/v2/api/graphql'
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
        }
        self.date = None
        self.topic = None
        self.search_term = None

    def filter_by_date(self, date):
        self.date = date

    def filter_by_topic(self, topic):
        self.topic = topic

    def filter_by_search_term(self, search_term):
        self.search_term = search_term

    def get_products(self, max_results=50):
        query = """
        query($after: DateTime, $topic: String, $first: Int) {
          posts(first: $first, postedAfter: $after, topic: $topic) {
            edges {
              node {
                id
                name
                tagline
                description
                url
                votesCount
                website
                commentsCount
                createdAt
                featuredAt
                slug
                reviewsCount
                reviewsRating
                thumbnail {
                  url
                }
                topics(first: 5) {
                  edges {
                    node {
                      name
                    }
                  }
                }
                user {
                  id
                  name
                }
                makers {
                  id
                  name
                }
              }
            }
          }
        }
        """

        variables = {
            "after": self.date.isoformat() if self.date else None,
            "topic": self.topic,
            "first": max_results
        }

        try:
            response = requests.post(self.api_url, json={'query': query, 'variables': variables}, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()

            if 'data' in data and 'posts' in data['data']:
                posts = data['data']['posts']['edges']
                products = [post['node'] for post in posts]
                
                if self.search_term:
                    products = self.filter_by_search(products)
                
                return products, None
            else:
                error_message = "Unexpected response structure"
                if 'errors' in data:
                    error_message += f": {data['errors']}"
                return [], error_message
        except requests.exceptions.RequestException as e:
            return [], f"Request error: {str(e)}"
        except Exception as e:
            return [], f"Unexpected error: {str(e)}"

    def filter_by_search(self, products):
        if not self.search_term:
            return products

        search_term = self.search_term.lower()
        return [
            product for product in products
            if search_term in product['name'].lower() or
            search_term in product['tagline'].lower() or
            search_term in product['description'].lower()
        ]