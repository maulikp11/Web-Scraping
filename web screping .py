#!/usr/bin/env python
# coding: utf-8

# In[107]:



import requests
from time import sleep
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs


# In[108]:


url = 'https://mars.nasa.gov/news/'


# In[109]:


response = requests.get(url)
# Create BeautifulSoup object; parse with 'lxml'
soup = bs(response.text, 'lxml')


# In[110]:


type(soup)
print(soup.prettify())


# In[111]:


title = soup.find("div",class_="content_title").text
news = soup.find('div', class_='rollover_description_inner').text
print(title)
print(news)


# In[112]:



executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=True)


# In[113]:


url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[114]:


html = browser.html
soup = bs(html, 'html.parser')
  
button = soup.find_all('a', class_='button fancybox')[0].get('data-link').strip()
button


# In[115]:


# Large Image
featured_image_url = soup.find_all('a', class_='fancybox')[1].get('data-fancybox-href')
featured_image_url

featured_image_url = url + featured_image_url
featured_image_url


# In[116]:


# Combine URL to make HTML.
html_page = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars' + button

browser.visit(html_page)
html_page


# In[117]:


url = 'https://twitter.com/marswxreport?lang=en'


# In[118]:


response = requests.get(url)
# Create BeautifulSoup object; parse with 'lxml'
soup = bs(response.text, 'lxml')

mars_weather = soup.find_all('p',                              class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")[0].text
# <p class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text" lang="en" data-aria-label-part="0">Sol 2312 (2019-02-06), high -13C/8F, low -72C/-97F, pressure at 8.13 hPa, daylight 06:47-18:53<a href="https://t.co/QpQemcmmJW" class="twitter-timeline-link u-hidden" data-pre-embedded="true" dir="ltr">pic.twitter.com/QpQemcmmJW</a></p>
print(mars_weather)


# In[119]:


url = 'https://space-facts.com/mars/'
tables = pd.read_html(url)
# print(tables)
df = tables[0]
df.columns=['Fact Name','Fact Value']
df['Fact Name']= df['Fact Name'].str.replace(':','')
df


# In[120]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[121]:


# URL Link to large image
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
# found on website
buttons = soup.find_all('a', class_='itemLink product-item')#[0].get('href').strip()
buttons


# In[122]:


urls = []
x=0
for button in buttons:
    urls.append(soup.find_all('a', class_='itemLink product-item')[x].get('href').strip())
    x=x+1

urls
urls = list(dict.fromkeys(urls))
urls


# In[123]:


image_url = 'https://astrogeology.usgs.gov'

image = []
title = []

print('')
print('Printing each website page , the URL of the main image, and the title')
print('')
for url in urls:
    button = url
    click_button = image_url + button
    print(click_button)

    browser.visit(click_button)
    html1 = browser.html
    soup = BeautifulSoup(html1, 'html.parser')
    main_image = soup.find_all('img', class_='wide-image')[0].get('src').strip()
    print(main_image)
    main_title =soup.find('h2', class_='title').text
    print(main_title)
    image.append(image_url + main_image)
    title.append(main_title)


# In[124]:


#dictionary for images and titles

dict_images = list(zip(image,title))
df = pd.DataFrame(dict_images, columns = ['image_url', 'title'])
df.to_dict('records')


# In[ ]:




