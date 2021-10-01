# Packages 

import re
import ast
import time
import random
import requests
import datetime
import numpy as np
import pandas as pd
from dateparser import parse
from tqdm.notebook import tqdm

from bs4 import BeautifulSoup

from GoogleNews import GoogleNews

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from transformers import pipeline
from transformers import AutoModelForCausalLM
from transformers import MarianMTModel, MarianTokenizer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Conversation, ConversationalPipeline, pipeline

from facebook.fbscrap import FBScraper

googlenews = GoogleNews(lang = 'en', region = 'CO')

class FbBot:
    def __init__(self, transformer=True) -> None:
        self.fb = FBScraper()
        if transformer:
            self.speach_blenderbot()
    
    # Open account 
    def launch_chrome(self):         
        options = Options()
        options.add_argument("--incognito")
        self.browser = webdriver.Chrome("E:\\Documents\\Projects\\Cloud\\browser_drivers\\chromedriver.exe", options = options)
        
        return self.browser

    def launch_firefox(self):         
        options = Options()
        options.add_argument("--incognito")
        self.browser = webdriver.Chrome("E:\\Documents\\Projects\\Cloud\\browser_drivers\\geckodriver.exe", options = options)
        
        return self.browser
    
    def typing(self, text, element, start, stop, step, precision): 
        for char in text:            
            f = 1 / precision
            n = random.randrange(start * f, stop * f, step * f) / f
            time.sleep(n)
            element.send_keys(char)

    def FB_account_opener(self, username, password): 
        # Open browser
        self.browser = self.launch_chrome()
        
        # Navigate to mobile facebook 
        self.browser.get("https://m.facebook.com/")
        
        # Login
        time.sleep(random.random()*5)
        email_box = self.browser.find_element_by_id('m_login_email')
        if email_box:
            self.typing(username, email_box, 0, 0.3, 0.01, 0.01)
        else:
            return 'Failed to input username'
            
        time.sleep(random.random()*5)
        password_box = self.browser.find_element_by_id('m_login_password')
        if password_box:
            self.typing(password, password_box, 0, 0.3, 0.01, 0.01)
        else:
            return 'Failed to input password'

        time.sleep(3)
        login_button = self.browser.find_element_by_name('login')
        if login_button:
            login_button.click()
        else:
            return 'Failed to click'
        
        time.sleep(4)
        
        self.browser.get('https://m.facebook.com')
        
        return self.browser

    # Friend requests 

    def receive_friend_request(self, user): 
        
        user.get('https://m.facebook.com/friends/center/requests/')
        request_page_source = BeautifulSoup(user.page_source , "html.parser")
        raw_header = request_page_source.find('header')        
        if raw_header:            
            header_text = raw_header.text            
            if 'Friend Requests' in header_text:
                raw_number_requests = raw_header.find('span')
                if raw_number_requests:                        
                    number_requests_str = raw_number_requests.text.strip()
                    if number_requests_str != '':
                        number_requests = int(number_requests_str)
                        if number_requests > 0:
                            return number_requests
                        else:
                            return False
                else:                    
                    return False            
            else:                
                return False        
        else:            
            return False

    def confirm_friend_request(self, user): 
        
        user.get('https://m.facebook.com/friends/center/requests/')        
        confirm_button = user.find_element_by_xpath('//button[@type="submit" and @value="Confirm"]')
        confirm_button.click()

    # Messenger 

    def open_messenger(self, user):             
        user.get("https://m.facebook.com/messages/")

    def send_message(self, user, text): 
        chat_box = user.find_element_by_xpath('//textarea[@name="body"]')
        chat_box.send_keys(text)
        send_button = user.find_element_by_xpath('//button[@type="submit" and @value="Send"]')
        send_button.click()

    def find_conversations(self, user):         
        conversations = user.find_elements_by_xpath('//div[@data-sigil="touchable"]')
        person_element_dict = {element.text.splitlines()[0]:element for element in conversations}        
        pattern = re.compile(r"\((\d+)\)")        
        unread_messeges = {person:element for person,element in person_element_dict.items() if pattern.findall(person) != []}
        read_messages = {person:element for person,element in person_element_dict.items() if pattern.findall(person) == []}
        
        return unread_messeges, read_messages

    def read_conversation(self, user): 
        
        while True: 
            try: 
                user.find_element_by_xpath('//*[ text() = "See Older Messages"]').click()
            except: 
                break
                
        chat_inputs = user.find_elements_by_xpath('//div[@class="voice acw" and @data-sigil="message-xhp marea"]')
        if chat_inputs != []: 
            chat_content = [(ast.literal_eval(row.get_attribute('data-store').replace('false', 'False'))['name'], row.text) for row in chat_inputs]
            conversation_flow = []
            for row in chat_content[:-1]: 

                source = row[0]
                content = " ".join([elm.strip() for elm in row[1].splitlines()[:-1]])

                if len(conversation_flow) == 0:
                    conversation_flow.append([source, content])

                else: 

                    if source == conversation_flow[-1][0]:
                        conversation_flow[-1][1]  = conversation_flow[-1][1] + " " + content

                    else:
                        conversation_flow.append([source, content])
                        
            return conversation_flow, " ".join([elm.strip() for elm in chat_content[-1][1].splitlines()[:-1]])
        
        else:            
            return None

    def generate_response(self, blenderbot_model, history, last_message): 
        conversation = Conversation("")

        for content in history: 
            if content[1] == 'Scraper Scrapington':
                conversation.append_response(content[1])
            else:
                conversation.add_user_input(content[1])
            conversation.mark_processed()
        conversation.add_user_input(last_message)

        reply = blenderbot_model([conversation])        
        response = reply.generated_responses[0].strip()

        return response
    
    def typing_from_place(self, text, driver, start, stop, step, precision):             
        for char in text:            
            f = 1 / precision
            n = random.randrange(start * f, stop * f, step * f) / f
            time.sleep(n)
            actions = ActionChains(driver)
            actions.send_keys(char)
            actions.perform()
        
        actions = ActionChains(driver)
        actions.send_keys(Keys.ENTER)
        actions.perform()

    def send_response(self, user, response): 
        
        text_box = user.find_element_by_xpath('//textarea[@id="composerInput" and @name="body"]')
        self.typing(response, text_box, 0, 0.3, 0.01, 0.01)        
        time.sleep(1)
        text_send = user.find_element_by_xpath('//button[@type="submit" and @value="Send" and @name="send"]')
        text_send.click()

    def speach_blenderbot(self):
        # Load blenderbot model 

        # Load tokenizer 
        blenderbot_tokenizer = AutoTokenizer.from_pretrained("facebook/blenderbot-3B")
        # Load model 
        blenderbot_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/blenderbot-3B")
        # Build pipeline 
        self.blenderbot_pipeline = ConversationalPipeline(model = blenderbot_model, tokenizer = blenderbot_tokenizer)


    def messaging_bot(self, user):         
        self.open_messenger(user)
        time.sleep(random.random()*5)

        unread, read = self.find_conversations(user)
        time.sleep(random.random()*5)
        
        print("Unread: ", len(unread))
        print("Read: ", len(read))
        
        if len(unread) > 0:
            random_index = random.randint(0, len(unread.values())-1)
            print(random_index)
            
            list(unread.values())[random_index].click()
            time.sleep(random.random()*5)
            
        else:
            random_index = random.randint(0, len(unread.values())-1)
            print(random_index)
            
            list(read.values())[random_index].click()
            time.sleep(random.random()*5)

        history, last_message = self.read_conversation(user)
        time.sleep(random.random()*5)

        if hasattr(self, 'blenderbot_pipeline'):
            response = self.generate_response(self.blenderbot_pipeline, history, last_message)
        else:
            print("Warning: Build blenderbot pipeline")
            response = ":)"
        time.sleep(random.random()*5)

        self.send_response(user, response)

    # Likes 

    def find_likes(self, user): 
        
        user.get('https://m.facebook.com')        
        time.sleep(random.random()*5)        
        like_buttons = user.find_elements_by_xpath('//a[@role="button" and @data-sigil="touchable ufi-inline-like like-reaction-flyout"]')
        
        return like_buttons

    def liking_bot(self, user): 
        
        like_buttons = self.find_likes(user)         
        if len(like_buttons) > 0:            
            random_index = random.randint(0, len(like_buttons)-1)            
            print(random_index)            
            like_button = like_buttons[random_index]            
            like_button.click()            
            time.sleep(random.random()*5)        
        else:            
            return None

    # Comments 

    def find_comments(self, user):         
        time.sleep(random.random()*5)        
        comments_buttons = user.find_elements_by_xpath('//a[@data-sigil="feed-ufi-focus feed-ufi-trigger ufiCommentLink mufi-composer-focus"]')
               
        return comments_buttons

    def num_comment_scraper(self, user): 
        
        source = BeautifulSoup(user.page_source, 'html.parser')            
        test = source.find("div", id = "m_story_permalink_view")        
        if test:             
            raw_comment_container = test.find_all("div", class_ = "_14v5")            
            return len(raw_comment_container)        
        else:            
            return None

    def get_post_text(self, user): 
        source = BeautifulSoup(user.page_source, 'html.parser')
        post_content_raw = source.find("div", class_ = "story_body_container") 
        raw_text = post_content_raw.find("div", class_ = "_5rgt _5nk5")
        if raw_text:
            MainText   = raw_text.text.strip()
        else: 
            MainText = None
        return MainText

    def post_comment(self, user, post_text, blenderbot_model): 

        text_area = user.find_element_by_xpath('//textarea[@id="composerInput" and @data-sigil="textarea mufi-composer m-textarea-input"]')

        if text_area:             
            comment_text = self.generate_response(blenderbot_model, [], post_text)
            self.typing(comment_text, text_area, 0, 0.3, 0.01, 0.01)
            comment_post_button = user.find_element_by_xpath('//button[@type="submit" and @value="Post" and @aria-label="Post" and @name="submit"]')
            comment_post_button.click()
        else:
            return None

    def commenting_bot(self, user, minimum_num_comments): 
        user.get('https://m.facebook.com')
        time.sleep(random.random()*5)

        comment_buttons = self.find_comments(user)
        time.sleep(random.random()*5)

        print("Number of comment buttons found: ", len(comment_buttons))

        if len(comment_buttons) > 0:
            random_index = random.randint(0, len(comment_buttons)-1)
            comment_buttons[random_index].click()
            time.sleep(random.random()*5)
            num_comments = self.num_comment_scraper(user)

            print('Number of comments found on this post', num_comments)
            if type(num_comments) == int:
                if num_comments > minimum_num_comments: 
                    post_text = self.get_post_text(user)
                    self.post_comment(user, post_text, self.blenderbot_pipeline)
                else: 
                    print('Not enough comments')
                    user.get('https://m.facebook.com')
            else:
                print('No comments found')
                user.get('https://m.facebook.com')
        else:
            print('No posts found')
            user.get('https://m.facebook.com')

    # Shares 

    def find_shares(self, user): 
        
        user.get('https://m.facebook.com')        
        time.sleep(random.random()*5)        
        shares_buttons = user.find_elements_by_xpath('//a[@data-sigil="share-popup"]')    
        
        return shares_buttons

    def sharing_bot(self, user):         
        share_buttons = self.find_shares(user)            
        if len(share_buttons) > 0:            
            random_index = random.randint(0, len(share_buttons)-1)
            print(random_index)            
            share_button = share_buttons[random_index]            
            share_button.click()            
            time.sleep(random.random()*5)            
            final_share_button = user.find_element_by_xpath('//a[@role="button" and @rel="ignore" and @id="share-one-click-button" and @data-sigil="touchable touchable share-one-click-button"]')        
            final_share_button.click()            
        else:            
            return None
        
    # Scrolling 

    def scrolling_bot(self, user): 

        user.get('https://m.facebook.com')        
        old_height = user.execute_script("return document.body.scrollHeight") # Initiate page height 
        for iter_ in np.arange(random.randint(1, 20)):
            user.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll once
            # Get new page height
            new_height = user.execute_script("return document.body.scrollHeight")
            # If after 60 seconds new height does not exceed old height, declare end of page 
            if new_height <= old_height:
                print('Reached end of page.')
                break
            else:
                old_height = new_height            
            time.sleep(4)
    
    # Posting 

    def write_post(self):        
        googlenews.search('Colombia')
        text = random.choice(googlenews.get_texts())            
        post = self.generate_response(self.blenderbot_pipeline, [], text)
        
        return text + ". " +  post

    def posting_bot(self, user): 
        
        post_page_button = user.find_element_by_xpath('//div[@tabindex="0" and @role="button" and @class="_4g34 _6ber _78cq _7cdk _5i2i _52we"]')
        time.sleep(random.random()*5)        
        post_page_button.click()        
        time.sleep(random.random()*5)        
        post_textbox = user.find_element_by_xpath('//textarea[@class="composerInput mentions-input" and @data-sigil="composer-textarea m-textarea-input"]')
            
        text = self.write_post()        
        self.typing(text, post_textbox, 0, 0.3, 0.01, 0.01)
        
        time.sleep(random.random()*5)        
        post_button = user.find_element_by_xpath('//button[@type="submit" and @value="Post" and @data-sigil="touchable submit_composer"]')
        time.sleep(random.random()*5)
        
        user.execute_script("arguments[0].click();", post_button)    
        time.sleep(random.random()*5)
        
        try: 
            user.get('https://m.facebook.com/')
        except:
            pass