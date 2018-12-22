# import dependencies 

from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time 
import datetime as dt

def scrape_info():

    # @NOTE: Replace the path with your actual path to the chromedriver
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    #return Browser('chrome', **executable_path, headless=False)
    news_title, news_p = mars_latest_news(browser)
    feat_img = mars_feat_img(browser)
    weather = mars_weather(browser)
    facts = mars_facts(browser)
    hemis = mars_hemi(browser)
    mars_data = {
            "news_title":news_title, 
            "news_paragraph":news_p,
            "featured_image":feat_img,
            "weather":weather,
            "facts":facts,
            "hemispheres":hemis,
            "last_scrape": dt.datetime.now()}
            
    print(mars_data)
    # Close browser
    browser.quit()
    # return results
    return(mars_data)
   

def mars_latest_news(browser):
    # Visit visitcostarica.herokuapp.com
    news = []
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #%%
    item_list = soup.find('ul', class_='item_list')

    news_title= item_list.find('div', class_='content_title').text
    news.append(news_title)
    news_p = item_list.find('div', class_='article_teaser_body').text
    news.append(news_p)
    #%%
    #print(news_title)
    print(news_p)
    #print(news)
    return news_title, news_p
def mars_feat_img(browser):
    # ### JPL Mars Space Images - Featured Image
    # * Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    # image url
    image_url = "https://www.jpl.nasa.gov/spaceimages/"
    browser.visit(image_url)
    time.sleep(1)
    featured_image = browser.find_by_id('full_image')
    featured_image.click()
    time.sleep(3)
    more_info = browser.find_link_by_partial_text('more info')
    more_info.click()
    html = browser.html
    soup = bs(html, 'html.parser')
    src_img = soup.find('figure',class_='lede').find('img')['src']
    #print(src_img)
    image_url = f'https://www.jpl.nasa.gov{src_img}'
    #print(image_url)
    return(image_url)
def mars_weather(browser):
    # ### Mars Weather 
    # * Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. 
    # Save the tweet text for the weather report as a variable called `mars_weather`.
    weather_url = "https://twitter.com/marswxreport"
    browser.visit(weather_url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    mars_weather = soup.find('div',class_='js-tweet-text-container').find('p',class_='TweetTextSize').get_text()
    #print(mars_weather)
    return(mars_weather)
def mars_facts(browser):
    # ### Mars Facts
    # 
    # * Visit the Mars Facts webpage [here](http://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # 
    # * Use Pandas to convert the data to a HTML table string
    table_url = 'https://space-facts.com/mars/'
    table_facts_html = requests.get(table_url)
    table_facts_df = pd.read_html(table_facts_html.text)[0]
    table_facts_df.columns = ['Description', 'Value']
    table_facts_df
    html_string = table_facts_df.to_html()
    html_string = html_string.replace('\n','')

    #print(html_string) 
    return(table_facts_df)
def mars_hemi(browser):   
    # ### Mars Hemispheres
    # * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)
    #  to obtain high resolution images for each of Mar's hemispheres.
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    time.sleep(1)

    hemi_urls = []
    links = browser.find_by_tag('h3')

    for i in range(len(links)):
        hemis =  {}
        browser.find_by_tag('h3')[i].click()
        sample = browser.find_link_by_text('Sample').first
        hemis['url'] = sample['href']
        hemis['title'] = browser.find_by_css('h2.title').text
        hemi_urls.append(hemis)
        browser.back()
        time.sleep(1)        
    #print(hemi_urls)
    return(hemi_urls)
#init_browser()
#scrape_info()


