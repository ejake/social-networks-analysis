from facebook_scraper import get_posts
from facebook_scraper import exceptions

import json, time, random
from facebook_scraper.fb_types import Credentials
from tqdm import tqdm
import pickle

import pandas as pd
import numpy as np

# Target profiles (Excel file)
DATA_URL = 'https://drive.google.com/uc?export=download&id=1Go5E3o7WGOINEGScblOnwiJQMbsxo5h9'
INPUT_TARGET = 'target_profiles.xlsx'
# OUTPUT PATH
OUTPUT_PATH = '/home/administrador/output-facebook/'
# CREDENTIALS
FBLOGINS_PATH = './fb_accounts.json'
# PARAMETERS
PAGES = 100

def save_data(name, list_data):
  """
  Save post and commends as pickle file
  """
  pickle.dump( list_data, open(name+"_{}.p".format(
    str(time.localtime()[0]) + \
      str(time.localtime()[1]) + \
        str(time.localtime()[2])), 'wb') )

def load_credentials():
  with open(FBLOGINS_PATH, 'r') as f:
    credentials = json.load(f)
  accounts = list(map(lambda x: tuple(x.values()), credentials["accounts"]))
  return accounts


def scrap_comments(accounts = []):
  # Scrap post and commnents
  print('Scraping...')
  interruptions = 0
  lst_postncomments = []
  for rw in tqdm(df_target_profiles.iloc[-8:].iterrows()):  
    lst_tg = []
    print(rw[1]['account'])
    try:
      if len(accounts) > 0:
        rdm_account = random.randint(0, len(accounts)-1)
        posts = get_posts(rw[1]['account'], 
                          pages = PAGES, 
                          extra_info=True, 
                          credentials=accounts[rdm_account],
                          options={"comments": True})
      else:
        posts = get_posts(rw[1]['account'], 
                          pages = PAGES, 
                          extra_info=True, 
                          options={"comments": True})

      for post in tqdm(posts):
        time.sleep(random.randint(1,4))
        lst_postncomments.append(post)
        lst_tg.append(post)
      
      time.sleep(random.randint(1,5))
      df_target_profiles.at[rw[0], 'getPosts'] = 1
      df_target_profiles.at[rw[0], 'getComments'] = 1
      save_data(OUTPUT_PATH + 'post_comments_' + rw[1]['account'], lst_tg)
    except exceptions.TemporarilyBanned:
      print("\nTemporarily Banned!")
      print("stopped in posts of id {}".format(rw[1]['account']))
      #time.sleep(3700)
      interruptions += 1
      break
    except exceptions.AccountDisabled:
      print("\Account Disiabled")
      print("stopped in posts of id {}".format(rw[1]['account']))
      break
    except exceptions.LoginError:
      print("\Login Error")
      print("with account {}".format(accounts[rdm_account]))
    #except:
     # print("Exception scraping posts of id {}".format(rw[1]['account']))
     # df_target_profiles.at[rw[0], 'getPosts'] = -1
     # df_target_profiles.at[rw[0], 'getComments'] = -1
     # interruptions += 1
    finally:
      save_data(OUTPUT_PATH + 'postncomments', lst_postncomments)


if __name__ == "__main__":
    print("Scrapping post and comments from:")
    # Load Input data
    df_target_profiles = pd.read_excel(DATA_URL)
    print(df_target_profiles.info())
    scrap_comments(load_credentials())
    print("###...Scraping finished successfully...###")
