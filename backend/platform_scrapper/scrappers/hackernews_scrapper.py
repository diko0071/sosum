import requests
from datetime import datetime, timedelta

class HackerNewsScraper:
    BASE_URL = "https://hacker-news.firebaseio.com/v0"

    def __init__(self):
        self.session = requests.Session()
        self.filter_timestamp = None

    def get_item(self, item_id):
        response = self.session.get(f"{self.BASE_URL}/item/{item_id}.json")
        return response.json() if response.status_code == 200 else None

    def filter_by_date(self, date):
        if isinstance(date, datetime):
            self.filter_timestamp = int(date.timestamp())
        elif isinstance(date, str):
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                self.filter_timestamp = int(date_obj.timestamp())
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        else:
            raise ValueError("Invalid date type. Use datetime object or string in YYYY-MM-DD format.")

    def get_stories(self, story_type, max_results=100):
        story_ids = self.session.get(f"{self.BASE_URL}/{story_type}stories.json").json()
        stories = []

        for item_id in story_ids:
            item = self.get_item(item_id)
            if item and self._is_valid_date(item):
                stories.append(item)
                if len(stories) >= max_results:
                    break

        return stories

    def _is_valid_date(self, item):
        if not self.filter_timestamp:
            return True
        return item['time'] >= self.filter_timestamp
    
    def _is_before_filter_date(self, item):
        if not self.filter_timestamp:
            return False
        return item['time'] < self.filter_timestamp

    def set_order(self, stories, order_by='score', reverse=True):
        if not stories:
            return []
        if order_by not in stories[0]:
            raise ValueError(f"Invalid order_by criterion: {order_by}")
        
        return sorted(stories, key=lambda x: x.get(order_by, 0), reverse=reverse)

    def get_posts(self, max_results=100):
        return self.get_stories("top", max_results)

    def get_asks(self, max_results=100):
        return self.get_stories("ask", max_results)
    
    def filter_by_keyword(self, stories, keyword):
        keyword = keyword.lower()
        filtered_stories = []

        for story in stories:
            title = story.get('title', '').lower()
            text = story.get('text', '').lower()

            if keyword in title or keyword in text:
                filtered_stories.append(story)

        return filtered_stories