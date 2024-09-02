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
        self.posted_after = None
        self.posted_before = None
        self.topic = None
        self.featured = None
        self.order = None
        self.search_term = None

    def filter_by_date_range(self, start_date, end_date):
        self.posted_after = start_date
        self.posted_before = end_date

    def filter_by_topic(self, topic):
        self.topic = topic

    def filter_by_featured(self, featured):
        self.featured = featured

    def set_order(self, order):
        self.order = order

    def filter_by_search_term(self, search_term):
        self.search_term = search_term

    def get_products(self, max_results=50):
        query = """
        query($after: String, $before: String, $featured: Boolean, $first: Int, $order: PostsOrder, $postedAfter: DateTime, $postedBefore: DateTime, $topic: String) {
          posts(
            after: $after,
            before: $before,
            featured: $featured,
            first: $first,
            order: $order,
            postedAfter: $postedAfter,
            postedBefore: $postedBefore,
            topic: $topic
          ) {
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
            "first": max_results,
            "postedAfter": self.posted_after.isoformat() if self.posted_after else None,
            "postedBefore": self.posted_before.isoformat() if self.posted_before else None,
            "topic": self.topic,
            "featured": self.featured,
            "order": self.order,
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
        
    def filter_by_date(self, date):
        self.posted_after = date
        self.posted_before = date + timedelta(days=1)

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
  

    def get_all_topics(self):
        query = """
        query($after: String, $first: Int) {
          topics(after: $after, first: $first, order: FOLLOWERS_COUNT) {
            pageInfo {
              hasNextPage
              endCursor
            }
            edges {
              node {
                id
                name
                slug
              }
            }
          }
        }
        """

        all_topics = {}
        has_next_page = True
        after = None

        try:
            while has_next_page:
                variables = {
                    "first": 100,
                    "after": after
                }
                
                response = requests.post(self.api_url, json={'query': query, 'variables': variables}, headers=self.headers)
                response.raise_for_status()
                
                data = response.json()

                if 'data' in data and 'topics' in data['data']:
                    topics = data['data']['topics']['edges']
                    for topic in topics:
                        all_topics[topic['node']['slug']] = topic['node']['name']
                    
                    page_info = data['data']['topics']['pageInfo']
                    has_next_page = page_info['hasNextPage']
                    after = page_info['endCursor']
                else:
                    has_next_page = False
                    if 'errors' in data:
                        raise Exception(f"GraphQL errors: {data['errors']}")

            return sorted(all_topics.items(), key=lambda x: x[1])
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")