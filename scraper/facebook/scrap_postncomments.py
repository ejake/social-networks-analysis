from facebook_scraper import get_posts
from facebook_scraper import exceptions

import json, time, random
from tqdm import tqdm
import pickle

import pandas as pd
import numpy as np

DATA_URL = 'https://drive.google.com/uc?export=download&id=1Go5E3o7WGOINEGScblOnwiJQMbsxo5h9'
INPUT_TARGET = 'target_profiles.xlsx'

print("Scrapping post and comments from:")
df_target_profiles = pd.read_excel(DATA_URL)
print(df_target_profiles.info())


def save_data(name, list_data):
  pickle.dump( list_data, open(name+"_{}.p".format(str(time.localtime()[0]) + str(time.localtime()[1]) + str(time.localtime()[2])), 'wb') )

# Scrap post and commnents
print('Scraping...')
lst_postncomments = []
for rw in tqdm(df_target_profiles.iloc[-13:].iterrows()):  
  lst_tg = []
  print(rw[1]['account'])
  try:
    for post in get_posts(rw[1]['account'], 
                          pages = 100, 
                          extra_info=True, 
                          credentials=("leodatom", "Moscow$101"),
                          options={"comments": True}):
      lst_postncomments.append(post)
      lst_tg.append(post)
      time.sleep(random.randint(1,3))
    df_target_profiles.at[rw[0], 'getPosts'] = 1
    df_target_profiles.at[rw[0], 'getComments'] = 1
    save_data('/home/ubuntu/output/post_comments_' + rw[1]['account'], lst_tg)
  except exceptions.TemporarilyBanned:
    print("\nTemporarily Banned!")
    print("stopped in account id {}".format(rw[1]['account']))
    break
  except exceptions.AccountDisabled:
    print("\Account Disiabled")
    print("stopped in commenter id {}".format(com_id))
    break
  except:
    df_target_profiles.at[rw[0], 'getPosts'] = -1
    df_target_profiles.at[rw[0], 'getComments'] = -1
  finally:
     save_data('/home/ubuntu/output/ex_post_comments_', lst_postncomments)

# Save post and commends as pickle file

pickle.dump( lst_postncomments, 
            open("/home/ubuntu/output/postsncommentns_{}.p".format(
                str(time.localtime()[0]) + str(time.localtime()[1]) + str(time.localtime()[2])),
                 "wb" ) )
