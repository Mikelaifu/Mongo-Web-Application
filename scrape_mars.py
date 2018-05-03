import pymongo
from bs4 import BeautifulSoup 
import pymongo 
from pprint import pprint 
import pandas as pd
import requests
from splinter import Browser
import json
import tweepy
import os
import time
from config import consumer_key, consumer_secret, access_token, access_token_secret
from pprint import pprint
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser = tweepy.parsers.JSONParser())
    


def mars_news():
  
    browser = Browser('chrome', headless=False)
    url1 = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url1)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    results= soup.find_all('div', class_= "image_and_description_container")
    title_list = []
    para_list = []
    mars_para = {}
    mars_title = {}
    for i in range(4):
        title = results[i].find("div", class_ = "content_title").text
        title_list.append(title)
        paragraph = results[i].find('div', class_="article_teaser_body").text
        para_list.append(paragraph)
   
    if title_list and para_list:
        mars_list = [
            {"Title":  title_list[0]}, 
            {"Paragraph" : para_list[0]}
        ]
#         print("-------------")
#         print("title:", title_list[0] )
#         print("Paragraph: ", para_list[0])
    return mars_list
# -----------------------------------------------------------------------------------------------------
def mars_weather():
    mars_weather_dict = {}
    public_tweets = api.user_timeline('@MarsWxReport')
    tweetlist = []
    for tweet in public_tweets:
        tweetlist.append(tweet)
        latest_tweet = tweetlist[0]['text']
    mars_weather_dict["lastest_tweet"] = latest_tweet
    return mars_weather_dict


# -------------------------------------------------------------------------------------------
def mars_Images():
    from splinter import Browser
    from bs4 import BeautifulSoup
    image_dict = {}
    browser = Browser('chrome', headless=False)
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(3)
    browser.click_link_by_id("full_image")
    elem = browser.find_link_by_partial_href("PIA")
    image_url = elem['href']
    browser.quit()
    browser2 = Browser('chrome', headless=False)
    url2 = image_url
    browser2.visit(url2) 
    browser2 = Browser('chrome', headless=False)
    url2 = image_url
    browser2.visit(url2)
    elem = browser2.find_link_by_partial_href("/spaceimages/images")
    featured_image_url = elem['href']
    
    
    image_dict["featured_image_url"] = featured_image_url
    
    return image_dict
# -------------------------------------------------------------------------------------------
def Mars_Table_fact():
    table = {}
    url = "https://space-facts.com/mars/"
    planet_table = pd.read_html(url)
    df = planet_table[0]

    df.columns = ['Elements', "data"]
    html_table = df.to_html(header=None,index=False)

    html_table = html_table.replace('\n', '')
    table["Fact_table"] = html_table
    
    return table

# -------------------------------------------------------------------------------------------------
def scrap_hemisphereInfo():
    
    from splinter import Browser
    from bs4 import BeautifulSoup
    # get branch links and name:
    browser = Browser('chrome', headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    # loop to spiders the name and links info
    title_names = soup.find_all("div", class_ = "description")
    titles = []
    branch_links = []
    for title_name in title_names:
        
        # loop get the links ready 
        link = title_name.a['href']
        href = f"https://astrogeology.usgs.gov/{link}"
        branch_links.append(href)
        
        # get the names ready 
        name = title_name.h3.text
        titles.append(name.replace(" Enhanced", "").strip())
        
    hemisphere_image_urls = []
    dictt = {}

    for i in range(len(branch_links)):
        browser = Browser('chrome', headless=False)
        url = branch_links[i]
        browser.visit(url)
        full_image_link = browser.find_link_by_text("Sample")
        image_link = full_image_link['href']
        dictt['title'] = titles[i]
        dictt['image_url'] = image_link
        hemisphere_image_urls.append(dictt)

    return hemisphere_image_urls

#  ------------------------scraping all functions-------------------------------
def scrape():
    import pymongo
    from bs4 import BeautifulSoup 
    import pymongo 
    from pprint import pprint 
    import pandas as pd
    import requests
    from splinter import Browser
    import json
    import tweepy
    import os
    import time
    from config import consumer_key, consumer_secret, access_token, access_token_secret
    from pprint import pprint
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser = tweepy.parsers.JSONParser())
    listt = mars_news()

    final_dict = {


    "MarsNews_title" : listt[0], 
    "MarsNews_paragraph" : listt[1], 
    "mars_weather" : mars_weather(),
    "Mars_image" : mars_Images(),
    "Mars_fact_table" :  Mars_Table_fact(),
    "Hemisphere_list" :  scrap_hemisphereInfo()

    }
    
    # if final_dict:

    #     print(final_dict)

    return final_dict
    
#scrap()
#---------------------------------insert final_dict into mongoDB--------------------------
# def insertmongo(dictionary):
#     import pymongo
#     conn = 'mongodb://localhost:27017'
#     client = pymongo.MongoClient(conn)
    
#     db= client.mars_db
    
#     db.mars.drop()
#     time.sleep(3)
#     collection = db.mars
#     collection.insert_one(dictionary)
#     mar_dict = collection.find()
    
#     # if  mar_dict :
        
#     #     print("Insert Successfully")
#     #    # print(mar_dict)
   
#     return mar_dict

#----------------------------call mongoDB function----------------------------------------

# insertmongo(scrap())
    
        
    




