from linkedin_api import Linkedin


class LinkedinScrapper:
    def __init__(self, email, password):
        self.api = Linkedin(email, password)

    def get_profile(self, username):
        return self.api.get_profile(username)

    def get_profile_posts(self, username, max_results=10):
        return self.api.get_profile_posts(username, post_count=max_results)
    
    def get_profile_updates(self, username, max_results=10):
        return self.api.get_profile_updates(username, max_results=max_results)


        