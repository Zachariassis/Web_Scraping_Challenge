from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import json
import time

#executable_path = {'executable_path': 'chromedriver.exe'}
#browser = Browser('chrome', **executable_path)

#Write out URLs
#url_mars_news='https://mars.nasa.gov/news/'
#url_space_images='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
#url_facts='https://space-facts.com/mars/'
#url_hemi='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

def mars_news():
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




def scrape_images():
    #Parse Space Images
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path)
    url_space_images='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_space_images)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    article=soup.find_all('ul', class_='articles')[0].find_all('li',class_='slide')[0]
    featured_image_url='https://www.jpl.nasa.gov'+article.find('div', class_='img').img['src']

    browser.quit()

    return featured_image_url




def scrape_facts():
    #Parse facts
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path)
    url_facts='https://space-facts.com/mars/'
    browser.visit(url_facts)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    article=soup.table.find_all('tr')

    table_data=pd.DataFrame({'Property':[],'Value':[]})
    for i in range(len(article)):
        p=article[i].find('td', class_='column-1').text
        v=article[i].find('td', class_='column-2').text
        table_data=table_data.append(pd.DataFrame({'Property':[p],'Value':[v]}))

    table_data=table_data.reset_index(drop=True)


    #Covert to HTML String
    html_data=table_data.to_html()
    text_file = open("data_table.html", "w")
    text_file.write(html_data)
    text_file.close()

    browser.quit()

    return table_data

def scrape_hemi():
    #Parse Hemispheres
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path)
    url_hemi='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemsisphere_url=pd.DataFrame({'Title':[], 'Img_url':[]})

    for i in range(4):
        browser.visit(url_hemi)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        article=soup.find_all('div', class_='item')
        link=article[i].a['href']
        browser.visit('https://astrogeology.usgs.gov'+link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url=soup.li.a['href']
        img_name=str.split(soup.h2.text)
        hemsisphere_url=hemsisphere_url.append(pd.DataFrame({'Title':[img_name[0]+' '+img_name[1]], 'Img_url':[img_url]}))
    hemsisphere_url=hemsisphere_url.reset_index(drop=True)

    browser.quit()

    return hemsisphere_url