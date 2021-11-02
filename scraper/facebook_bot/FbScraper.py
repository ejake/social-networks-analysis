from facebook_bot.FbBot import FbBot

import datetime
from dateparser import parse


from bs4 import BeautifulSoup

# Demographic scraping 

def profile_scraper(user, profile): 
    """
    Input: user: browser with and facebook account login
           profile: Facebook profile URL
    Output: about_content dictionary including profile information 
            (if it is available) about: education, work, 
    ex. profile_data = profile_scraper(user, 'https://m.facebook.com/AndreaOchoaL97/about?lst=100047716653194%3A1421843452%3A1632837488')
    Refactoring: Too long function
    """
    
    user.get(profile)
    source = user.page_source
    soup = BeautifulSoup(source, "html.parser")
    
    about_content = {}
    b = soup.find('div', {'id':'timelineBody'})

    raw_education_container = b.find('div', {'id':'education'})
    educational_units = []
    if raw_education_container:
        raw_education_containers = raw_education_container.find_all("div", class_ = '_5cds')
        if raw_education_containers != []: 
            for raw_edu_container in raw_education_containers:        
                edu_container = raw_edu_container.find('div', class_ = '_2pir')
                if edu_container:
                    raw_edu_units = edu_container.find_all('span')
                    if raw_edu_units != []:
                        educational_unit = []
                        for raw_edu_unit in raw_edu_units:
                            edu_unit = raw_edu_unit.text
                            if edu_unit not in educational_unit:
                                educational_unit.append(edu_unit)

                        educational_units.append(", ".join(educational_unit))
        about_content['Education'] = educational_units

    raw_education_container = b.find('div', {'id':'work'})
    work_units = []
    if raw_education_container:
        raw_education_containers = raw_education_container.find_all("div", class_ = '_5cds')
        if raw_education_containers != []: 
            for raw_edu_container in raw_education_containers:        
                edu_container = raw_edu_container.find('div', class_ = '_2pir')
                if edu_container:
                    raw_edu_units = edu_container.find_all('span')
                    if raw_edu_units != []:
                        educational_unit = []
                        for raw_edu_unit in raw_edu_units:
                            edu_unit = raw_edu_unit.text
                            if edu_unit not in educational_unit:
                                educational_unit.append(edu_unit)

                        work_units.append(", ".join(educational_unit))
        about_content['Work'] = work_units

    raw_living_container = b.find('div', {'id':'living'})
    living_units = []
    if raw_living_container:
        raw_living_units = raw_living_container.find_all("div", {'class':'_4g34', 'aria-hidden':'true'})
        if raw_living_units != []: 
            for raw_living_unit in raw_living_units:
                living_unit = raw_living_unit.find('h4')
                if living_unit:            
                    if living_unit.text not in living_units:
                        living_units.append(living_unit.text)
        about_content['Places'] = living_units 

    raw_info_container = b.find('div', {'id':'basic-info'})
    info_units = {}
    if raw_info_container:
        raw_info_containers = raw_info_container.find_all("div", class_ = '_5cds')
        if raw_info_containers != []: 
            for raw_info_container in raw_info_containers:  
                info_container = raw_info_container.find('div', class_ = 'lr')
                info_unit = [elm.text for elm in info_container.find_all('div') if elm.text != '']
                info_units[info_unit[1]] = info_unit[0]
        about_content['Info'] = info_units
    
    return about_content


def date_cleaner(raw_input, datetime_format):     
    if type(raw_input) == str:            
        raw_input = raw_input.replace('թ.','')
        raw_input = raw_input.replace('ժամը','')
        raw_input = raw_input.replace('ին:','')        

        if "Yesterday" in raw_input:
            time_of_day = raw_input.split(" at ")[-1]
            day = str(datetime_format.year) + "-" + str(datetime_format.month) + "-" + str(datetime_format.day - 1) + "-" + time_of_day    
            clean_date = parse(day)
        elif "mins" in raw_input:
            num_mins = int(raw_input.replace(" mins", ""))
            clean_date = datetime_format - datetime.timedelta(minutes = num_mins)
        elif "min" in raw_input:
            clean_date = datetime_format - datetime.timedelta(minutes = 1)
        elif "hrs" in raw_input:
            num_hrs = int(raw_input.replace(" hrs", ""))
            clean_date = datetime_format - datetime.timedelta(hours = num_hrs)
        elif "hr" in raw_input:
            clean_date = datetime_format - datetime.timedelta(hours = 1)
        elif "at" in raw_input:
            if "," in raw_input:
                clean_date = parse(raw_input)
            else:
                clean_date = parse(raw_input + " " + str(datetime.datetime.now().year))
        else:
            clean_date = parse(raw_input)
            if clean_date:
                return clean_date
            else:
                return raw_input
        return clean_date        
    else:
        return raw_input

def link_scraper(browser, page_link, target_date): 
    """
    Page link scraper
    """
    # Navigate to page link
    browser.get(page_link)
    
    # Convert target date to datetime 
    datetime_target_date = parse(target_date)

    print("Start Scrolling")
    all_posts = None # Initiate container for post source code
    start = datetime.datetime.now() # Initiate start time 
    old_height = browser.execute_script("return document.body.scrollHeight") # Initiate page height 
    while True:
        now = datetime.datetime.now() # Get current time
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll once

        # Get page source 
        page = browser.page_source 
        page = BeautifulSoup(page, "html.parser")

        # Check if at end of page every 60 seconds 
        if now > start + datetime.timedelta(seconds = 60):
            start = now
            # Get new page height
            new_height = browser.execute_script("return document.body.scrollHeight")
            # If after 60 seconds new height does not exceed old height, declare end of page 
            if new_height <= old_height:
                all_posts = page.find_all("article")
                print('Reached end of page.')
                break
            else:
                old_height = new_height
        # Get post containers loaded so far 
        post_container = page.find_all("article")
        # If posts found
        if post_container != []:
            # Get last post
            last_post = post_container[-1] 
            # Get header of last post
            last_post_header = last_post.find("header") 
            if last_post_header:
                # Get source for link container, which contains the date of the post 
                raw_links_container = last_post_header.find_all("a", {"href" : True})
                if raw_links_container != []:
                    date_container_list = [elm for elm in raw_links_container if "story.php?" in elm["href"] or 
                                                                                 "/events/"   in elm["href"] or 
                                                                                 "/photos/"   in elm["href"] or 
                                                                                 "/photo.php" in elm["href"]]
                    if date_container_list != []:
                        # Get raw date
                        date_raw   = date_container_list[-1].text
                        # Format to datetime using date_cleaner function 
                        date_clean = date_cleaner(date_raw, now)
                        print(date_raw, date_clean, "\n")

                        # If we have passed the target date, stop scrolling 
                        if date_clean < datetime_target_date:

                            print("Scrolling complete.")
                            all_posts = post_container
                            break

                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            pass
            print("Scroll error.")
            return page
    
    # Isolate good posts; code is similar to above
    good_posts = []
    for post in all_posts:        
        post_header = post.find("header")        
        if post_header:            
            raw_links_container = post_header.find_all("a", {"href" : True})            
            if raw_links_container != []:
                date_container_list = [elm for elm in raw_links_container if "story.php?" in elm["href"] or 
                                                                             "/events/"   in elm["href"] or 
                                                                             "/photos/"   in elm["href"] or 
                                                                             "/photo.php" in elm["href"]]
                if date_container_list != []:
                    good_posts.append(post)                
                else:
                    pass
            else:
                pass
        else:
            pass
    
    # Extract post link from good post 
    all_links = []
    for post in good_posts:        
        raw_link_container = post.find_all("a", {"href" : True}) 
        if raw_link_container != []:            
            post_link_container = []
            for raw_link in raw_link_container:                
                if "story.php?" in raw_link['href']:                    
                    link = "https://m.facebook.com/" + raw_link["href"]
                    post_link_container.append(link)            
            all_links.append(post_link_container)
    all_links_single = [links[0] for links in all_links if len(links) != 0]    
    print("Found " + str(len(all_links_single)) + " posts.")
    
    return all_links_single