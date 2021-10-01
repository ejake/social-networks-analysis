from tqdm import tqdm
import pandas as pd
from facebook_scraper import get_profile
from facebook_scraper import exceptions
import json, time, random

from fbscrap import FBScraper

DIRECT_DOWNLOAD_URL = 'https://drive.google.com/uc?export=download&id=1kOT1xCZ6NEkEmPaqfpmfoTok30Vqd-2K'
OUTPUT_DATA = '/home/administrador/output-facebook/profiles_data_{}.json'

def read_ids():
    df = pd.read_csv(DIRECT_DOWNLOAD_URL, names=['commenter_id'])
    df = df.astype({'commenter_id' : str})
    print(df.info())
    return df


def scrap_profile(com_id):    
    time.sleep(random.randint(2,5))
    profile = []
    
    profile = get_profile(com_id) 
    
    return profile

def save_profiles(list_data):
    with open(
        OUTPUT_DATA.format(
            str(time.localtime()[0]) + \
                str(time.localtime()[1]) + \
                    str(time.localtime()[2])),
                    'w') as fp:
        json.dump(list_data, fp)

if __name__ == "__main__":
    df_profiles = read_ids()
    fb = FBScraper()
    if len(fb.scrap_posts()) > 0:
        ids = df_profiles.commenter_id.unique()
        list_profiles = []
        iters = 37
        for id in tqdm(ids[37:]):
            try:
                list_profiles.append(scrap_profile(id))
                iters += 1
                if iters % 30 == 0:
                    print('Waiting a long time to escape banning')
                    time.sleep(random.randint(1800,3600))
                    print('Resuming scraping...')
            except exceptions.TemporarilyBanned:
                print("\nTemporarily Banned!")
                print("stopped in {} iteration, commenter id {}".format(iters, id))
                break
            finally:
                save_profiles(list_profiles)
    save_profiles(list_profiles)
