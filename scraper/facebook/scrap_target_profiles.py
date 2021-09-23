from facebook_scraper import get_profile

import json, time, random
from tqdm import tqdm

import pandas as pd
import numpy as np


DATA_URL = 'https://drive.google.com/uc?export=download&id=1Go5E3o7WGOINEGScblOnwiJQMbsxo5h9'
INPUT_TARGET = 'target_profiles.xlsx'
OUTPUT_DATA = 'profiles_target_{}.json'

# Load Input data

df_target_profiles = pd.read_excel(DATA_URL)
print(df_target_profiles.info())


#Scrap profiles
lst_profiles = []
for rw in tqdm(df_target_profiles.iterrows()):
  time.sleep(random.randint(1,3))
  try:
    lst_profiles.append(get_profile(rw[1]['account']))
    df_target_profiles.at[rw[0], 'getProfile'] = 1
  except:
    df_target_profiles.at[rw[0], 'getProfile'] = -1

    
print(df_target_profiles.getProfile.value_counts())

# Save profiles as JSON file

with open(
    OUTPUT_DATA.format(
        str(time.localtime()[0]) + str(time.localtime()[1]) + str(time.localtime()[2])),
         'w') as fp:
    json.dump(lst_profiles, fp)
    
# Save Log File

df_target_profiles.to_excel(INPUT_TARGET,index=False)
