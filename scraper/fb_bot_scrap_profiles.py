from facebook_bot.FbBot import FbBot
import facebook_bot.FbScraper as fbs

from azure.BlobStorage import BlobStorage

from tqdm import tqdm
import pandas as pd
import json, time, random

import requests
import shutil


def read_ids(csv_url, id_column):
    df = pd.read_csv(csv_url, names=[id_column])
    df = df.astype({id_column : str})
    print(df.info())
    return df


def scrap_profile(browser, id, url_prefix):    
    time.sleep(random.randint(5,45))
    profile_data = fbs.profile_scraper(browser, url_prefix.format(id)) 
    
    return profile_data

def scrap_profile_image(browser, id, url_prefix):    
    time.sleep(random.randint(5,45))
    print("Scraping image from {}".format(url_prefix+id))
    url_image = fbs.image_profile_scraper(browser, url_prefix+id) 

    return url_image

def save_profiles(list_data, id, path_prefix):
    with open(
        path_prefix.format( str(id),
            str(time.localtime()[0]) + \
                str(time.localtime()[1]) + \
                    str(time.localtime()[2])),
                    'w') as fp:
        json.dump(list_data, fp)

def save_profile_image(url_pic, id, **kwargs):
    print("Saving image: {}".format(url_pic))
    r = requests.get(url_pic, stream = True)
    filename = './temp_image_profile.jpg'
    output_file_name = kwargs['file_name'].format(str(id),
                                                  str(time.localtime()[0]) + \
                                                      str(time.localtime()[1]) + \
                                                          str(time.localtime()[2]))
    if kwargs["local_path"]:
        filename = "{}{}".format(kwargs["local_path"], output_file_name)
    if r.status_code == 200: #  image retrieved successfully
        r.raw.decode_content = True
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)

        if kwargs["blobstorage"]:
            dest = "{}/{}".format(kwargs['sink_folder'], output_file_name)
            kwargs["blobstorage"].upload_file(filename, dest)
    else:
        print("Image can't be retreived")

def open_account(fb_bot, open_browser = False):
    rdm_account = random.randint(0, len(fb_bot.fb.accounts)-1)
    user = fb_bot.FB_account_opener(username = fb_bot.fb.accounts[rdm_account][0], 
                                    password = fb_bot.fb.accounts[rdm_account][1],
                                    open_browser = open_browser)
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
    # 1. Load configuration parameters
    conf_param = json.load(open('./config_scraper.json', 'r'))
    if conf_param['output']['AZURE']:
        conf_param_azure = json.load(open('./azure/config_blob.json', 'r'))
        CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix=core.windows.net'.format(
                            conf_param_azure['STORAGEACCOUNTNAME'], 
                            conf_param_azure['STORAGEACCOUNTKEY'])
        blobs = BlobStorage(CONNECTION_STRING, 
                            conf_param_azure['CONTAINERNAME'])
    # 2. Get id profiles from csv file
    df_profiles = read_ids(conf_param['input']['DIRECT_DOWNLOAD_URL'], 
                           conf_param['input']['profile_id_column'])
    # 3. Initiate Scraper bot
    if conf_param['facebook']['auto_author']:
        fb = FbBot(transformer = True)
    else:
        fb = FbBot(transformer = False)
    # 4. Open browser session
    if conf_param['facebook']['open_browser']:
        user = open_account(fb, True)
    else:
        user = open_account(fb)
    # 5. Scraping iterations paramenters
    iters = 0
    exception_iters  = 0
    start = 11513
    ids = df_profiles.commenter_id.unique()
    start_time =  time.time()

    #for id in tqdm(ids[start:]):
    for id in ids[10:20]:
        try:            
            if conf_param['facebook']['download_data']:# Scrap profile data
                print("{}: Scraping {} profile data".format(iters, id))
                profile = scrap_profile(user, id, conf_param['output']['ABOUT_URL'])
                profile["account_id"] = id
                save_profiles(profile, id, conf_param['output']['LOCAL_FILE'])
            if conf_param['facebook']['download_image']:# Scrap profile image
                print("{}: Scraping {} profile image".format(iters, id))
                image_url = scrap_profile_image(user, id, conf_param['facebook']['FB_URL'])
                if not (image_url):
                    continue
                if conf_param['output']['local']:
                    if conf_param['output']['AZURE']:
                        save_profile_image(image_url, id, 
                                        sink_folder = conf_param_azure["BLOBNAME-IMAGES"],
                                        file_name = conf_param['output']['OUTPUT_IMAGE'],
                                        local_path = conf_param['output']['LOCAL_PATH'],
                                        blobstorage = blobs)
                    else:
                        save_profile_image(image_url, id, 
                                        file_name = conf_param['output']['OUTPUT_IMAGE'],
                                        local_path = conf_param['output']['LOCAL_PATH'])
                else:
                    if conf_param['output']['AZURE']:
                        save_profile_image(image_url, id, 
                                        sink_folder = conf_param_azure["BLOBNAME-IMAGES"],
                                        file_name = conf_param['output']['OUTPUT_IMAGE'],
                                        blobstorage = blobs)

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

