from facebook_bot.FbBot import FbBot

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