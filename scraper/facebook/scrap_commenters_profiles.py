import gdown
import pickle

import pandas as pd

from facebook_scraper import get_profile

import json, time, random

DATA_URL =  'https://drive.google.com/uc?export=download&id=18odYk5Ot5UIlAfV_LQGW4VGbePOpDaC8'
DATA_FILE = 'postncomments.p'

gdown.download(DATA_URL, DATA_FILE, quiet=False)

lst_postsncomments = pickle.load( open( DATA_FILE, "rb" ) )


# Load raw data in a data frame
columns_posts = ['post_id', 
                 'comments', 
                 'likes',
                 'reaction_count',
                 'text',
                 'time',
                 'user_id',
                 'username',
                 'shares',
                 'shared_user_id']
df_posts = pd.DataFrame(columns=columns_posts)
comments_key = 'comments_full'
columns_comments = ['post_id',
                    'comment_id', 
                    'commenter_id',
                    'commenter_name',
                    'comment_time',
                    'comment_text']
df_comments = pd.DataFrame(columns=columns_comments)

def get_row(dict_data, target_column):
  lst_row = []
  for key in target_column:
    try:
      value = dict_data[key]
    except:
      value = 'Null'
    lst_row.append(value)

  return lst_row

for post in tqdm(lst_postsncomments):
  #print(get_row(post, columns_posts))
  # Save posts in dataframe
  row = pd.Series(get_row(post, columns_posts), 
                  index=df_posts.columns)
  df_posts = df_posts.append(row,
                             ignore_index = True)
  #print(row['post_id'])
  if len(post[comments_key]) > 0:
    for comment in post[comments_key]:      
      row_comment = pd.Series(get_row(comment, columns_comments), 
                              index=df_comments.columns)
      row_comment['post_id'] = row['post_id']
      df_comments = df_comments.append(row_comment, 
                                       ignore_index = True)
"""
Scrap commenters profiles
"""      
      
lst_profiles_commenters = []
lst_log_fail = []

for com_id in tqdm(df_comments.commenter_id.unique()):
  time.sleep(random.randint(1,3))
  try:
    lst_profiles_commenters.append(get_profile(com_id))
  except exceptions.TemporarilyBanned:
    print("\nTemporarily Banned!")
    print("stopped in commenter id {}".format(com_id))
    break
  except:
    lst_log_fail.append(com_id)
    
print("Profiles successfully scraped: {}".format(len(lst_profiles_commenters)))
print("Profiles failled scraped: {}".format(len(lst_log_fail)))

# Save data
pickle.dump( lst_profiles_commenters, 
            open("commenters_profile_{}.p".format(
                str(time.localtime()[0]) + str(time.localtime()[1]) + str(time.localtime()[2])),
                 "wb" ) )

pickle.dump( lst_log_fail, 
            open("log_fail_commenters_profile_{}.p".format(
                str(time.localtime()[0]) + str(time.localtime()[1]) + str(time.localtime()[2])),
                 "wb" ) )
