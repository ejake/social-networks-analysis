from facebook_bot.FbBot import FbBot
import facebook_bot.FbScraper as fbs

from tqdm import tqdm
import pandas as pd
import json, time, random

#from fbscrap import FBScraper

DIRECT_DOWNLOAD_URL = 'https://drive.google.com/uc?export=download&id=1kOT1xCZ6NEkEmPaqfpmfoTok30Vqd-2K'
OUTPUT_DATA = '/home/administrador/output-facebook/profile_{}_data_{}.json'

ABOUT_URL = 'https://m.facebook.com/{}/about'

def read_ids():
    df = pd.read_csv(DIRECT_DOWNLOAD_URL, names=['commenter_id'])
    df = df.astype({'commenter_id' : str})
    print(df.info())
    return df


def scrap_profile(browser, id):    
    time.sleep(random.randint(2,5))
    profile_data = fbs.profile_scraper(user, ABOUT_URL.format(id)) 
    
    return profile_data

def save_profiles(list_data, id):
    with open(
        OUTPUT_DATA.format( str(id),
            str(time.localtime()[0]) + \
                str(time.localtime()[1]) + \
                    str(time.localtime()[2])),
                    'w') as fp:
        json.dump(list_data, fp)

def open_account(fb_bot):
    rdm_account = random.randint(0, len(fb_bot.fb.accounts)-1)
    user = fb_bot.FB_account_opener(fb_bot.fb.accounts[rdm_account][0], fb_bot.fb.accounts[rdm_account][1])
    print("Using {} Facebook account".format(fb_bot.fb.accounts[rdm_account][0]))

    return user

def random_action(fb, user):
    #try:
    if (random.random() < 0.5):
        print("Scrolling...")
        fb.scrolling_bot(user) # Scrolling

    if random.random() < 0.2:
        print("Liking...")
        fb.liking_bot(user) # Liking

    if random.random() < 0.01:                                                                                                                                                      print("Sharing...")
        print("Sharing")
        fb.sharing_bot(user) # Sharing
        #if random.random() < 0.001
            #print('Posting...')
            #fb.posting_bot(user)
    #except:
    #    print("Error executing action on FB")


if __name__ == "__main__":
    df_profiles = read_ids()
    fb = FbBot(transformer = False)
    user = open_account(fb)   
    iters = 0
    exception_iters  = 0
    start = 171
    ids = df_profiles.commenter_id.unique()
    for id in tqdm(ids[start:]):
        try:
            print("{}: Scraping {} profile".format(iters, id))
            profile = scrap_profile(user, id)
            save_profiles(profile, id)
            iters += 1
            exception_iters = 0           
            if iters % 10 == 0:
                delay_s = random.randint(1, 100)
                print('Waiting {} seconds to escape banning'.format(delay_s))
                time.sleep(delay_s)
                print('Resuming scraping...')
            else:
                random_action(fb, user)
            if (iters % 20 == 0) and (random.random() < 0.95):
                #user.quit()
                delay_s =  random.randint(100, 1000)
                print('Waiting {} seconds to escape banning'.format(delay_s))
                time.sleep(delay_s)
                print('Resuming scraping...')
                #user = open_accont(fb)                    
        except AttributeError:
            print("\nFail scraping {} in iteration {}".format(id, iters))
            exception_iters +=1
            if exception_iters > 3:
                user.quit()
                print('Waiting 1 hour for banning')
                time.sleep(3600)
                user = open_account(fb)
            if exception_iters > 5:
                print("\n6 consecutive exceptions reached, aborting execution")
                break
            #user.quit()
    #user.quit()


