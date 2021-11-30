from facebook_bot.FbBot import FbBot
import facebook_bot.FbScraper as fbs
import time

fb = FbBot(transformer=False)
print('Abriendo Browser:')
time.sleep(10)
user = fb.FB_account_opener('leodatom','Panama$123', open_browser=True)

#fb.posting_bot(user)

#profile_data = fbs.profile_scraper(user, 'https://m.facebook.com/AndreaOchoaL97/about?lst=100047716653194%3A1421843452%3A1632837488')
#profile_data = fbs.profile_scraper(user, 'https://m.facebook.com/carloss.nietoo/about')
#profile_data = fbs.profile_scraper(user, 'https://m.facebook.com/565399728/about')
#https://m.facebook.com/565399728/about?lst=100073194427747%3A100001483860077%3A1634123545&ref=m_notif&notif_t=group_recommendation
#https://m.facebook.com/100054881895968/about?lst=100073194427747%3A100001483860077%3A1634123545&ref=m_notif&notif_t=group_recommendation
#https://m.facebook.com/100054881895968/about?lst=100073194427747%3A100001483860077%3A1634123545&ref=m_notif&notif_t=group_recommendation
#'https://m.facebook.com/100000002175639/about'

#https://m.facebook.com/profile.php?id=100054881895968&ref=m_notif&notif_t=group_recommendation
#https://m.facebook.com/profile.php?id=100054881895968&v=info&lst=100073194427747%3A100054881895968%3A1634123190&ref=m_notif&notif_t=group_recommendation
#https://m.facebook.com/100054881895968/about
#https://m.facebook.com/profile.php?id=100054881895968&_rdr
#https://m.facebook.com/profile.php?id=100054881895968&ref=m_notif&notif_t=group_recommendation
#https://m.facebook.com/lizethjhoanna.bocanegravera?groupid=4291572777538340&ref=m_notif&notif_t=group_recommendation
#https://m.facebook.com/lizethjhoanna.bocanegravera/about&ref=m_notif&notif_t=group_recommendation
#https://m.facebook.com/565399728/about?lst=100073194427747%3A100001483860077%3A1634123545&ref=m_notif&notif_t=group_recommendation



#links = fbs.link_scraper(user, 'https://m.facebook.com/BancoDavivienda/', 'September 1, 2021')

#print(links)

#print(profile_data)
#fb.scrolling_bot(user)

#fb.messaging_bot(user)#error
#fb.sharing_bot(user)
#fb.liking_bot(user)

# Profile images
link = fbs.image_profile_scraper(user, 'https://m.facebook.com/100000002175639')
print(link)