from ntscraper import Nitter
from datetime import datetime

class TwitterScrapper:
    def __init__(self, log_level=1, skip_instance_check=False, instance=None):
        self.scraper = Nitter(log_level=log_level, skip_instance_check=skip_instance_check)
        self.instance = instance

    def get_user_info(self, username: str):
        return self.scraper.get_profile_info(username, mode='detail', instance=self.instance)

    def get_tweets(self, username: str, since=None, until=None, number=-1):
        since_str = since.strftime("%Y-%m-%d") if since else None
        until_str = until.strftime("%Y-%m-%d") if until else None
        
        return self.scraper.get_tweets(username, mode='user', number=number, since=since_str, until=until_str, instance=self.instance)

    def filter_tweets_by_date(self, tweets, since=None, until=None):
        if not since and not until:
            return tweets

        filtered_tweets = []
        for tweet in tweets:
            tweet_date = datetime.strptime(tweet['date'], "%Y-%m-%d %H:%M:%S %Z")
            if (not since or tweet_date >= since) and (not until or tweet_date <= until):
                filtered_tweets.append(tweet)

        return filtered_tweets