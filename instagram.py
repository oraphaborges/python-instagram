
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from decouple import config
from time import sleep
import requests

def get_images(tags,MAX_SCROLL = 1,output_dir='output/',login=False):
    if login:
        # LOGIN ON INSTAGRAM
        webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        sleep(3) # waiting time to load the page

        username = webdriver.find_element_by_name('username')
        username.send_keys(config('USENAME'))
        password = webdriver.find_element_by_name('password')
        password.send_keys(config('PASSWORD'))

        button_login = webdriver.find_element_by_css_selector("#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(4) > button")
        button_login.click()
        sleep(3)

    for tag in tags:
        webdriver.get(f'https://www.instagram.com/explore/tags/{tag}/')

        sleep(3)

        SCROLL = 0
        images_unique=[]
        # Get scroll height
        last_height = webdriver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(2)

            # Calculate new scroll height and compare with last scroll height
            new_height = webdriver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                webdriver.execute_script("window.scrollTo(document.body.scrollHeight,0);")
                break

            # This means that there is still photos to scrap
            if SCROLL < MAX_SCROLL:
                last_height = new_height 
            else:
                break
            SCROLL += 1
            sleep(2)

            # Retrive the html
            html_to_parse=str(webdriver.page_source)
            html=bs(html_to_parse,"html5lib")

            # Get the image's url
            images_url=html.findAll("img", {"class": "FFVAD"})

            # Check if they are unique
            in_first = set(images_unique)
            in_second = set(images_url)

            in_second_but_not_in_first = in_second - in_first

            result = images_unique + list(in_second_but_not_in_first)
            images_unique=result

        for i in range(len(images_unique)):
        # for i in range(5): # for teste
            # Save each image.jpg file
            name=f"{output_dir}{tag}_{i}.jpg"
            with open(name, 'wb') as handler:
                img_data = requests.get(images_unique[i].get("src")).content
                handler.write(img_data)

    #Close the webdriver   
    webdriver.close()

# LOADING BROWSER DRIVE
webdriver = webdriver.Chrome('drivers/chromedriver') 

# GOING TO SOME HASHTAG
tags = ['lasanha','guioza','pizza']
get_images(tags)