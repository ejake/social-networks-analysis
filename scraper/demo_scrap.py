from facebook_bot.FbBot import FbBot
import facebook_bot.FbScraper as fbs

fb = FbBot()
user = fb.FB_account_opener('leodatom','Moscow$101')
#fb.posting_bot(user)

#profile_data = fbs.profile_scraper(user, 'https://m.facebook.com/AndreaOchoaL97/about?lst=100047716653194%3A1421843452%3A1632837488')
profile_data = fbs.profile_scraper(user, 'https://m.facebook.com/carloss.nietoo/about')


