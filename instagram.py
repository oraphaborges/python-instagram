
from selenium import webdriver

# LOADING BROWSER DRIVE
webdriver = webdriver.Chrome('drivers/chromedriver')

# LOGIN ON INSTAGRAM
webdriver.get('https://www.instagram.com/')
