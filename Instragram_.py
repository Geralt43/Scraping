# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'

#%%
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np
from selenium.webdriver import Chrome
from random import choice
import json
import requests
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from pandas.io.json.normalize import nested_to_record
from datetime import datetime
#%%
df = pd.DataFrame(columns=('Links', 'Timestamp', 'caption', 's','full_name','likes','url','location'))
#%%
def insta_hashtag(hashtag_search):

    #Download https://chromedriver.chromium.org/downloads and set in your path

    #global variable
    global df
    
    browser = webdriver.Chrome('C:/Users/952820/Desktop/chromedriver')
    browser.get('https://www.instagram.com/explore/tags/'+hashtag_search)
    last_height = browser.execute_script("return document.body.scrollHeight")
    print(last_height)

    links=[]
    while True:
        Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        source = browser.page_source
        data=bs(source, 'html.parser')
        body = data.find('body')
        script = body.find('script', text=lambda t: t.startswith('window._sharedData'))
        page_json = script.text.split(' = ', 1)[1].rstrip(';')
        data = json.loads(page_json)
        new_height=browser.execute_script('return document.body.scrollHeight')
        print(new_height)
        for link in data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']:
            links.append('https://www.instagram.com'+'/p/'+link['node']['shortcode']+'/')
        
        if new_height>=40000:
            break
        last_height=new_height

    print('Links encontrados: ', links)

    for link in links:
        req = requests.get(link).text
        soup = BeautifulSoup(req, "html.parser")
        scripts = soup.find_all("script")
        for script in scripts:
            if script.text[:18] == "window._sharedData":
                break

        data = json.loads(script.contents[0][21:-1])
        df=df.append({'Links': link,'Timestamp': datetime.fromtimestamp(int(data["entry_data"]["PostPage"][0]["graphql"]
                ["shortcode_media"]["taken_at_timestamp"])),'caption':str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]
                ["edge_media_to_caption"]["edges"][0]["node"]["text"]),
                's':str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["owner"]["username"]),
                'full_name':str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["owner"]["full_name"]),
                'likes':str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_media_preview_like"]["count"]),
                'url':str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["display_url"]),
                'location':str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["location"])},ignore_index=True)
    df.to_excel('instagram_'+ str(hashtag_search) +'.xls')
    #df=[]    
    print("################Finish################################")

#%%


def trends_google(product,year_start,month_start,day_start,year_end, month_end, day_end,geo='',gprop='',sleep=0):
    pytrends=TrendReq(hl='Germany', tz=360)
    search=pytrends.get_historical_interest
    (product,year_start=year_start,month_start=month_start,day_start=day_start,year_end=year_end,
    month_end=month_end,day_end=day_end,geo=geo,gprop=gprop,sleep=sleep)

trends_google(i,2020,5,20,2020,6,7)

#%%

list_words=['Jasmin','Muskatellersalbei','Rosenöl','Neroli','Fenchel','Jojoba','cbd Öl',
            'Cannabis','Patschulioil','Ylangylangoil','Lavendel Öl','Whiterosemusk',
            'Mandarinoil','Geranienöl','Sandelholz','Mandarin',
            'Vanilleöl','Bergamotte','Palosanto','Zypressenöl','Rosmarinöl','Neemöl','Pfefferminz Öl'
            'Bernstein','Ingwer','Zimt','Rosa Grapefruit','Weihrauch','Kamille','salbei']

for i in list_words:
    insta_hashtag(i)

insta_hashtag('ätherischeöle')


#%%

       
        # print(json.dumps(data, indent=4))
        print("timestamp: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["taken_at_timestamp"]))
        
        print("caption: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]
                                ["edge_media_to_caption"]["edges"][0]["node"]["text"]))
        print("s: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["owner"]["username"]))
        print("full name: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["owner"]["full_name"]))
        #print("comments: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_media_to_comment"]["count"]))
        print("likes: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_media_preview_like"]["count"]))
        print("url: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["display_url"]))
        print("dimensions: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["dimensions"]))
        print("location: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["location"]))


    if(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["is_video"]):
        print("video: yes")
        print("video views: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["video_view_count"]))

    else:
        print("video: no")


def insta_details(urls):
    """Take a post url and return post details"""
    browser = webdriver.Chrome('C:/Users/952820/Desktop/chromedriver')
    post_details = []
    for link in urls:
        browser.get(link)
        try:
        # This captures the standard like count. 
            likes = browser.find_element_by_partial_link_text('likes').text
        except:
        # This captures the like count for videos which is stored
            xpath_view = '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/span'
            likes = browser.find_element_by_xpath(xpath_likes).text
        age = browser.find_element_by_css_selector('a time').text
        xpath_comment = '//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/li[1]/div/div/div'
        comment = browser.find_element_by_xpath(xpath_comment).text
        insta_link = link.replace('https://www.instagram.com/p','')
        post_details.append({'link': insta_link,'likes/views': likes,'age': age, 'comment': comment})
        time.sleep(10)
    return post_details
#%%
insta_details(['https://www.instagram.com/p/CBHoRxLB22j/','https://www.instagram.com/p/CBHoRxLj9lJ/'])


#%%
import pandas as pd
import time
from selenium.webdriver import Chrome


#%%
from random import choice
import json
 
import requests
from bs4 import BeautifulSoup
 
_user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
]
 
 
class InstagramScraper:
 
    def __init__(self, user_agents=None, proxy=None):
        self.user_agents = user_agents
        self.proxy = proxy
 
    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(_user_agents)
 
    def __request_url(self, url):
        try:
            response = requests.get(url, headers={'User-Agent': self.__random_agent()}, proxies={'http': self.proxy,
                                                                                                 'https': self.proxy})
            response.raise_for_status()
        except requests.HTTPError:
            raise requests.HTTPError('Received non 200 status code from Instagram')
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response.text
 
    @staticmethod
    def extract_json_data(html):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)
 
    def profile_page_metrics(self, profile_url):
        results = {}
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
        except Exception as e:
            raise e
        else:
            for key, value in metrics.items():
                if key != 'edge_owner_to_timeline_media':
                    if value and isinstance(value, dict):
                        value = value['count']
                        results[key] = value
                    elif value:
                        results[key] = value
        return results
 
    def profile_page_recent_posts(self, profile_url):
        results = []
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']["edges"]
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    results.append(node)
        return results
#%%
from pprint import pprint
 
k = InstagramScraper()
results = k.profile_page_recent_posts('https://www.instagram.com/iam_zeif/')
pprint(results)

#%%
#likes
posts = ['CBGhBEagV71']

for post in links:
    #post_url = 'https://www.instagram.com/p/{}/'.format(post)
    response = requests.get(post)
    soup = bs(response.content)
    sharedData = soup.find('script', text=re.compile('"mainEntityofPage"')).text
    likes = json.loads(sharedData.strip())['interactionStatistic']['userInteractionCount']
    print(post, '-', likes, 'likes')   


#%%


import requests
import json
from bs4 import BeautifulSoup
#links = 

for link in links:
    req = requests.get(link).text
    soup = BeautifulSoup(req, "html.parser")
    scripts = soup.find_all("script")
    for script in scripts:
        if script.text[:18] == "window._sharedData":
            break

    data = json.loads(script.contents[0][21:-1])
    # print(json.dumps(data, indent=4))
    print("timestamp: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["taken_at_timestamp"]))
    print("caption: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"][0]["node"]["text"]))
    print("s: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["owner"]["username"]))
    print("full name: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["owner"]["full_name"]))
    #print("comments: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_media_to_comment"]["count"]))
    print("likes: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_media_preview_like"]["count"]))
    print("url: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["display_url"]))
    print("dimensions: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["dimensions"]))
    print("location: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["location"]))


    if(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["is_video"]):
        print("video: yes")
        print("video views: " + str(data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["video_view_count"]))

    else:
        print("video: no")

    print("################################################")


#%%
