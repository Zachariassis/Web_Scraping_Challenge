from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import json
import time



def mars_news2():
    #Parse Mars News
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path)
    url_mars_news='https://mars.nasa.gov/news/'
    browser.visit(url_mars_news)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(2)


    article=soup.find_all('ul', class_='item_list')[0].find_all('li',class_='slide')

    title=[]
    news=[]
    for i in range(len(article)):
        title.append(article[i].find('div',class_='content_title').text)
        news.append(article[i].find('div',class_='article_teaser_body').text)
    
    news=pd.DataFrame({"Title": title, "Body": news})

    browser.quit()

    return news