from facebook_bot.FbBot import FbBot
import facebook_bot.FbScraper as fbs
import time

fb = FbBot(transformer=True)
print('Abriendo Browser:')
time.sleep(10)
user = fb.FB_account_opener('leodatom','Moscow$101', open_browser=True)

#fb.posting_bot(user)

#profile_data = fbs.profile_scraper(user, 'https://m.facebook.com/AndreaOchoaL97/about?lst=100047716653194%3A1421843452%3A1632837488')
#profile_data = fbs.profile_scraper(user, 'https://m.facebook.com/carloss.nietoo/about')
#profile_data = fbs.profile_scraper(user, 'https://m.facebook.com/565399728/about')

#print(profile_data)
#fb.scrolling_bot(user)

#fb.messaging_bot(user)#error
#fb.sharing_bot(user)
fb.liking_bot(user)