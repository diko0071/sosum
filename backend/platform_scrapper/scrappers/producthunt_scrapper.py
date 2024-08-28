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
        self.date = datetime.now().date()

    def filter_by_date(self, date):
        self.date = date

    def get_products(self, max_results=50):
        query = """
        query($date: Date!) {
          posts(first: $max_results, postedAfter: $date, postedBefore: $next_date) {
            edges {
              node {
                id
                name
                tagline
                description
                url
                votesCount
                website
                thumbnail {
                  url
                }
                topics {
                  edges {
                    node {
                      name
                    }
                  }
                }
              }
            }
          }
        }
        """

        variables = {
            "date": self.date.isoformat(),
            "next_date": (self.date + timedelta(days=1)).isoformat(),
            "max_results": max_results
        }

        response = requests.post(self.api_url, json={'query': query, 'variables': variables}, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            posts = data['data']['posts']['edges']
            return [post['node'] for post in posts]
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return []