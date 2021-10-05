import random
import json
from facebook_scraper import get_posts
from facebook_scraper import exceptions


class FBScraper:    

    def __init__(self):
        # CREDENTIALS
        self.FBLOGINS_PATH = './facebook/fb_accounts.json'
        self.DEMO_ACCOUNT = 'MyPharmacistHouse'
        self.accounts = self.load_credentials()

    def get_credentiasls(account):
        credentials = []
        if "account" in account:
            credentials.append(account["account"])
        elif "email" in account:
            credentials.append(account["email"])
        if "password" in account:
            credentials.append(account["password"])
        return tuple(credentials)

    def load_credentials(self):
        with open(self.FBLOGINS_PATH, 'r') as f:
            credentials = json.load(f)
        accounts = list(map(get_credentials, credentials["accounts"]))
        return accounts
    
    def scrap_posts(self):
        rdm_account = random.randint(0, len(self.accounts)-1)        
        lst_posts =  []
        posts = get_posts(self.DEMO_ACCOUNT, 
                          pages = 2, 
                          extra_info=True, 
                          credentials=self.accounts[rdm_account])
        for po in posts:
            lst_posts.append(po)
        return lst_posts
