#Import dependecies 
import sys
from splinter import Browser
from bs4 import BeautifulSoup as soup 
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 
import datetime as dt 



def scrape_all(): 
    #Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    #run all scraping functions and store results in a dictionary 
    data = {
        "news_title": news_title, 
        "mars_hemispheres": mars_hemispheres(browser),
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser), 
        "facts": mars_facts(), 
        "last_modified": dt.datetime.now()
    }
    browser.quit()
    return data

def mars_news(browser): 
    #visit the mars news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #option delay for lading the page 
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    #convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    #add try/execpt for the error handling 
    try: 
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        slide_elem.find("div", class_='content_title')
        #Use the parent element to find the first 'a' tag and save it as a 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        #Use the parent element to find the paragraph text 
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
            return None, None 

    return news_title, news_p

def featured_image(browser):
    #Visit Url 
    try: 
        PREFIX = "https://web.archive.org/web20181114023740"
        url = f'{PREFIX}/https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        article = browser.find_by_tag('article').first['style']
        article_background = article.split("_/")[1]/replace('"),',"")
        return 
        f'{PREFIX}_if/{article_background}'
    except: 
        return 'https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/pia22486-main.jpg'

def mars_facts():

    try: 
        #Use 'read_html' to scrape the facts into a datframe 
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException: 
        return None 

        #Assign columns and set index of dataframe
        df.columns=['Description', 'Mars']
        df.set_index('Description', inplace=True)
        #Convert dataframe into HTML format, add bootstrap 
        return df.to_html(classes="table table-striped")
    
    if __name__ == "__main__":
        #if running as script, as print scraped data 
        print(scrape_all())

def mars_hemispheres(browser): 
    url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    #soup2 = soup(html, 'html.parser')
    links = browser.find_by_css('a.product-item h3')
    print(len(links))
# 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    links = browser.find_by_css('a.product-item h3')
    for i in range(len(links)):
        hemisphere = {}
        browser.find_by_css('a.product-item h3')[i].click()
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href'] 
        print(sample_elem['href'])
        hemisphere['title'] = browser.find_by_css('h2.title').text
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    return hemisphere_image_urls




'''
    for link in soup_links:
        hemispheres ={}
        url_hemisphere = 'https://astrogeology.usgs.gov' + link.find_by_tag('a')['href']
        browser.visit(url_hemisphere)  
        html = browser.html
        title = browser.find_by_css('h2', class_='title').text
        print("This is the title" + title)
        img_url = soup2.find('img', class_='wide-image')['src']
        print("This is the url" + img_url)
        hemispheres["title"]= title
        hemispheres["img_url"]= 'https://astrogeology.usgs.gov' + img_url
        hemisphere_image_urls.append(hemispheres.copy())
# Print the list that holds the dictionary of each image url and title.
        print(hemisphere_image_urls)
    return hemisphere_image_urls 
'''