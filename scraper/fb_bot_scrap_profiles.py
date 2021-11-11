from facebook_bot.FbBot import FbBot
import facebook_bot.FbScraper as fbs

from tqdm import tqdm
import pandas as pd
import json, time, random

#from fbscrap import FBScraper

DIRECT_DOWNLOAD_URL = 'https://drive.google.com/uc?export=download&id=1kOT1xCZ6NEkEmPaqfpmfoTok30Vqd-2K'
OUTPUT_DATA = '/home/administrador/output-facebook/profile_{}_data_{}.json'

ABOUT_URL = 'https://m.facebook.com/{}/about'
#ABOUT_URL = 'https://m.facebook.com/{}/about?lst=100073194427747%3A100001483860077%3A1634123545&ref=m_notif&notif_t=group_recommendation'

def read_ids():
    df = pd.read_csv(DIRECT_DOWNLOAD_URL, names=['commenter_id'])
    df = df.astype({'commenter_id' : str})
    print(df.info())
    return df


def scrap_profile(browser, id):    
    time.sleep(random.randint(5,45))
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

def random_action(fb_bot, user):
    try:
        if (random.random() < 0.5):
            print("Scrolling...")
            fb_bot.scrolling_bot(user) # Scrolling

        if random.random() < 0.2:
            print("Liking...")
            fb_bot.liking_bot(user) # Liking

        if random.random() < 0.01: 
            print("Sharing")
            fb_bot.sharing_bot(user) # Sharing
        #if random.random() < 0.001
            #print('Posting...')
            #fb.posting_bot(user)
    except:
        print("Error executing action on FB")

def check_time(start, duration = 4):
    """
    Duration (hours)
    """
    flag_break = False
    if (time.time() - start) > (duration*3600):
        flag_break = True

    return flag_break


if __name__ == "__main__":
    df_profiles = read_ids()
    fb = FbBot(transformer = False)
    user = open_account(fb)   
    iters = 0
    exception_iters  = 0
    start = 11513
    ids = df_profiles.commenter_id.unique()
    start_time =  time.time()
    for id in tqdm(ids[start:]):
        try:
            print("{}: Scraping {} profile".format(iters, id))
            profile = scrap_profile(user, id)
            save_profiles(profile, id)
            iters += 1
            exception_iters = 0
            if check_time(start_time, 0.75):
                print("Stopping process, elapsing time longer than 3/4 hour")
                user.quit()
                break
            if iters % 10 == 0:
                delay_s = random.randint(1, 100)
                print('Waiting {} seconds to escape banning'.format(delay_s))
                time.sleep(delay_s)
                print('Resuming scraping...')
            else:
                random_action(fb, user)
            if (iters % 20 == 0) and (random.random() < 0.95):
                #user.quit()
                delay_s =  random.randint(10, 400)
                print('Waiting {} seconds to escape banning'.format(delay_s))
                time.sleep(delay_s)
                print('Resuming scraping...')
                #user = open_accont(fb)                    
        except AttributeError:
            print("\nFail scraping {} in iteration {}".format(id, iters))
            exception_iters +=1
            if exception_iters > 3:
                user.quit()
                print('Waiting 1/2 hour for banning')
                time.sleep(1800)
                user = open_account(fb)
            if exception_iters > 5:
                print("\n6 consecutive exceptions reached, aborting execution")
                break
        except IndexError:
            print("IndexError: skipping {} in iteration {}".format(id, iters))
            exception_iters += 1
            if exception_iters > 3:
                print("More than 3 consecutive exceptions, aboriting execution")
                break
            #user.quit()
    #user.quit()


