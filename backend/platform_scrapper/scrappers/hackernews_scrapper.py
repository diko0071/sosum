import requests
from datetime import datetime, timedelta

class HackerNewsScraper:
    BASE_URL = "https://hacker-news.firebaseio.com/v0"

    def __init__(self):
        self.session = requests.Session()

    def get_item(self, item_id):
        response = self.session.get(f"{self.BASE_URL}/item/{item_id}.json")
        return response.json() if response.status_code == 200 else None

    def get_stories(self, story_type, start_date=None, end_date=None, max_results=100):

        story_ids = self.session.get(f"{self.BASE_URL}/{story_type}stories.json").json()
        stories = []

        for item_id in story_ids[:max_results]:
            item = self.get_item(item_id)
            if item and self._is_within_date_range(item, start_date, end_date):
                stories.append(item)

        return stories

    def _is_within_date_range(self, item, start_date, end_date):
        if not start_date and not end_date:
            return True

        item_date = datetime.fromtimestamp(item['time'])
        
        if start_date and item_date < start_date:
            return False
        if end_date and item_date > end_date:
            return False
        
        return True

    def get_posts(self, start_date=None, end_date=None, max_results=100):

        return self.get_stories("top", start_date, end_date, max_results)

    def get_asks(self, start_date=None, end_date=None, max_results=100):

        return self.get_stories("ask", start_date, end_date, max_results)