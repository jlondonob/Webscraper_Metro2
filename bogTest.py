from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait             #wait until javascript data loads
from selenium.webdriver.common.keys import Keys                     #simulate pressing keys or buttons in webpage
from selenium.webdriver.chrome.options import Options               #add headless option to driver
from selenium.webdriver.support import expected_conditions as EC    #used with webdriverwait to wait until a certain condition is met
from selenium.webdriver.common.by import By    

from selenium.webdriver.support.ui import Select

import time 

url = "https://www.metrocuadrado.com/casa/venta/bogota/"

driver_path = '/Users/puchu/Desktop/WebScraper_Metro2/chromedriver'
chrome_options = Options()
chrome_options.add_argument('--headless')
webdriver = webdriver.Chrome(
    executable_path=driver_path,
    #options=chrome_options
)


with webdriver as driver:
    
    #wait object for later use
    wait = WebDriverWait(driver, 10)

    driver.get(url)  

    #accept cookies to remove banner
    accept_cookies_button = driver.find_element_by_css_selector('.disclamer-action a')
    accept_cookies_button.click()  

    #buttons
    min_area = driver.find_element_by_xpath("//div[label='Área (m²):']//div[@class='m2-select-container']")
    min_area.click()
    driver.find_element_by_xpath("//*[contains(text(), '60 m')]").click()

    max_area = driver.find_element_by_xpath("(//div[label='Área (m²):']//div[@class='m2-select-container'])[2]")
    max_area.click()
    driver.find_element_by_xpath("//*[contains(text(), '100 m')]").click()
    

    time.sleep(10)


    driver.close()