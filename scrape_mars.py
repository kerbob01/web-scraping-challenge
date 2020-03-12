# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
#browser = Browser('chrome')

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"web-scraping-challenge": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict ={}

##################################################################################################################

#Get 1st article of Mars news(title and paragraph)
browser = Browser('chrome')    
nasa_url = 'https://mars.nasa.gov/news/'
browser.visit(nasa_url)
html = browser.html
news_soup = bs(html, 'html.parser')
news_title = news_soup.find_all('div', class_='content_title')[1].text
print(news_title)
news_body = news_soup.find_all('div', class_='article_teaser_body')[0].text
print(news_body)

####################################################################################################################

 # Mars Image to be scraped
#browser = Browser('chrome') 
jpl_url = 'https://www.jpl.nasa.gov'
images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(images_url)
html = browser.html
images_soup = bs(html, 'html.parser')
    # Retrieve featured image link
relative_image_path = images_soup.find_all('img')[3]["src"]
featured_image_url = jpl_url + relative_image_path
print(relative_image_path)
print(featured_image_url)

#########################################################################################################################

# #Gets Mars weather from twitter
# weather_url = 'https://twitter.com/marswxreport?lang=en'
# browser.visit(weather_url)
# html = browser.html
# soup = bs(html, "html.parser")
# tweet_containers = soup.find_all('div', class_="js-tweet-text-container")
# print(tweet_containers[0].text)
# p = tweet_containers[0].text
# type(p)
# for tweets in tweet_containers:
#     if tweets.text:
#         print(tweets.text)
#         break

# for i in range(10):
#     tweets = tweet_containers[i].text
#     if "Sol " in tweets:
#         print(tweets)
#         break

#############################################################################################################################
 # Mars facts to be scraped, converted into html table
facts_url = 'https://space-facts.com/mars/'
facts = pd.read_html(facts_url)
#print(facts)
mars_facts_df = facts[2]
mars_facts_df.columns = ["Description", "Value"]
mars_html_table = mars_facts_df.to_html()
#mars_html_table.replace('\n', '')
print(mars_html_table)

##############################################################################################################################
#Gets a photo of each of Mars Hempsheres
hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(hemispheres_url)

html_hemispheres = browser.html

soup = bs(html_hemispheres, 'html.parser')

items = soup.find_all('div', class_='item')

hemisphere_image_urls = []

hemispheres_main_url = 'https://astrogeology.usgs.gov'

for item in items: 
    title = item.find('h3').text
    image_url = item.find('a', class_='itemLink product-item')['href']
    browser.visit(hemispheres_main_url + image_url)
    image_html = browser.html
    soup = bs( image_html, 'html.parser')
    image_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    hemisphere_image_urls.append({"Title" : title, "Image_URL" : image_url})

hemisphere_image_urls

################################################################################################################
#Creates a dictonary of all the data scraped from above

mars_dict = {
    "news_title": news_title,
    "news_body": news_body,
    "featured_image_url": featured_image_url,
    #"mars_weather": mars_weather,
    "fact_table": str(mars_html_table),
    "hemisphere_images": hemisphere_image_urls
    }

#print(mars_dict)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017"
conn = 'mongodb://localhost:27017'
#mongo = pymongo(app)
mongo = pymongo.MongoClient(conn)

db = mongo.mars_db

db.news.drop()

db.news.insert_one(mars_dict)

mars_dict = list(db.news.find_one())
#teams = list(db.team.find())
print(f'start mongo call')
print(mars_dict)
print(f'end mongo call')

###############################################################################################################
#closes Browser
browser.quit()
