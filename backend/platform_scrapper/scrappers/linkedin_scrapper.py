from linkedin_api import Linkedin
from requests.cookies import cookiejar_from_dict
import os

class LinkedinScrapper:
    def __init__(self, email, password, method='credentials'):
        if method == 'credentials':
            self.api = Linkedin(email, password)
        elif method == 'cookie':
            cookies = cookiejar_from_dict({
                'liap': 'true',
                'JSESSIONID': os.getenv('LINKEDIN_COOKIE_JSESSIONID'),
                'liat': os.getenv('LINKEDIN_COOKIE_LI_AT'),
            })
            self.api = Linkedin('', '', cookies=cookies)

    def get_profile(self, username):
        return self.api.get_profile(username)

    def get_profile_posts(self, username, max_results=10):
        return self.api.get_profile_posts(username, post_count=max_results)
    
    def get_profile_updates(self, username, max_results=10):
        return self.api.get_profile_updates(username, max_results=max_results)


        