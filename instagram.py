
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from decouple import config
from time import sleep


# LOADING BROWSER DRIVE
webdriver = webdriver.Chrome('drivers/chromedriver')

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

