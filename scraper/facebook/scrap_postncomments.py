from facebook_scraper import get_posts

import json, time, random
import pickle


DATA_URL = 'https://drive.google.com/uc?export=download&id=1Go5E3o7WGOINEGScblOnwiJQMbsxo5h9'
INPUT_TARGET = 'target_profiles.xlsx'

print("Scrapping post and comments from:")
df_target_profiles = pd.read_excel(DATA_URL)
print(df_target_profiles.info())


def save_data(name, list_data):
  with open(
    name+"_{}.json".format(
        str(time.localtime()[0]) + str(time.localtime()[1]) + str(time.localtime()[2])),
         'w') as fp:
    json.dump(list_data, fp)
    
# Scrap post and commnents

lst_postncomments = []
for rw in df_target_profiles.iterrows():  
  print(rw[1]['account'])
  try:
    for post in get_posts(rw[1]['account'], 
                          pages = 100, 
                          extra_info=True, 
                          credentials=("jakomlds", "Colombia$2021"),
                          options={"comments": True,
                                   "reactors": True}):
      lst_postncomments.append(post)
      time.sleep(random.randint(1,3))
    df_target_profiles.at[rw[0], 'getPosts'] = 1
    df_target_profiles.at[rw[0], 'getComments'] = 1
    save_data('post_comments_' + rw[1]['account'], 
              lst_postncomments)
  except exceptions.TemporarilyBanned:
    print("\nTemporarily Banned!")
    print("stopped in commenter id {}".format(com_id))
    break
  except:
    df_target_profiles.at[rw[0], 'getPosts'] = -1
    df_target_profiles.at[rw[0], 'getComments'] = -1

# Save post and commends as pickle file

pickle.dump( lst_postncomments, 
            open("postsncommentns_{}.p".format(
                str(time.localtime()[0]) + str(time.localtime()[1]) + str(time.localtime()[2])),
                 "wb" ) )
