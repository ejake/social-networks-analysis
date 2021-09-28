from tqdm import tqdm
import pandas as pd
from facebook_scraper import get_profile
from facebook_scraper import exceptions
import json, time, random

from fbscrap import FBScraper

DIRECT_DOWNLOAD_URL = 'https://drive.google.com/uc?export=download&id=1kOT1xCZ6NEkEmPaqfpmfoTok30Vqd-2K'
OUTPUT_DATA = 'profiles_data_'

def read_ids():
    df = pd.read_csv(DIRECT_DOWNLOAD_URL, names=['commenter_id'])
    print(df.info())
    return df


def scrap_profile(com_id):    
    time.sleep(random.randint(1,5))
    profile = []
    try:
        profile = get_profile(com_id) 
    except exceptions.TemporarilyBanned:
        print("\nTemporarily Banned!")
        print("stopped in commenter id {}".format(com_id))
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
        for id in tqdm(ids):
            list_profiles.append(scrap_profile(id))
    save_profiles(list_profiles)
