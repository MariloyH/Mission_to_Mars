#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Dependencies 
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 


# In[2]:


#Defining path and Browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title` 
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ## Featured images

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[14]:


df.to_html()


# # Deliverable 1:  Scrape High-Resolution Mars’ Hemisphere Images and Titles

# In[15]:


# 1. Use browser to visit the URL 
main_url = 'https://marshemispheres.com/'

browser.visit(main_url)


# In[16]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# In[17]:


# 3. Write code to retrieve the image urls and titles for each hemisphere.

# 3.1 Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

#3.2 Find information
hemisphere_items = img_soup.find_all('div', class_ = 'item')

for hemisphere in hemisphere_items:
    
    #Loop through the full-resolution image URL, click the link, 
    #find the Sample image anchor tag, and get the href.
    hmf_url = hemisphere.find('a', class_='itemLink product-item')['href']
    # Visit each hemisphere page.
    full_image_elem = browser.visit(main_url + hmf_url)
    
    # Parse HTML for retrieve hemisphere image 
    full_img_html = browser.html
    img_soup = soup(full_img_html, 'html.parser')

    # Retrieve full image source    
    hmf_title = img_soup.find('h2', class_='title').text
    hmf_url = main_url + img_soup.find('li').a.get('href')
    
    hemispheres = {}
    hemispheres['img_url'] = hmf_url
    hemispheres['title'] = hmf_title
    hemisphere_image_urls.append(hemispheres)
    
    # Browse back to repeat
    browser.back()


# In[18]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[19]:


#5 Quit the browser
browser.quit()

