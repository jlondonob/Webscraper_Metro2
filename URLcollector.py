from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait #para esperar a que pagina cargue JavaScript
from selenium.webdriver.common.keys import Keys #para escribir en la pagina
from selenium.webdriver.chrome.options import Options # add headless option to driver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import json

url = 'https://www.metrocuadrado.com/casas/venta/medellin/'
driver_path = '/Users/puchu/Desktop/WebScraper_Metro2/chromedriver'

chrome_options = Options()
chrome_options.add_argument('--headless')

webdriver = webdriver.Chrome(
    executable_path=driver_path,
    options=chrome_options
)

with webdriver as driver:
    
    # Open website stored in `url` object
    driver.get(url)  

    # Creates a web object that will be used later. It stores the following information
    # " This is a wait where the conection will time out if takes more than 10s to load"
    wait = WebDriverWait(driver, 10)

    # Removes cookies banner that is blocking the next page button by clicking on accept
    accept_cookies_button = driver.find_element_by_css_selector('.disclamer-action a')
    accept_cookies_button.click()  

    # Locates next page button for further use.  Also creates an empty arrow_disabled object
    next_page_button = driver.find_element_by_css_selector('.item-icon-next a')
    arrow_disabled = driver.find_elements_by_css_selector('.item-icon-next.page-item.disabled')

    links = driver.find_elements_by_css_selector('.card-result-img .sc-bdVaJa')
    links = [link.get_attribute('href') for link in links]

    while True:
        if len(arrow_disabled) > 0:
            print('No more pages left')
            break
        else:
            # Clicks next page and checks if button is disabled
            next_page_button.click()
            arrow_disabled = driver.find_elements_by_css_selector('.item-icon-next.page-item.disabled')

            # Only purpose of this chunk is testing. It may be deleted
            current_page=driver.find_element_by_css_selector('.page-item.active')

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.card-result-img .sc-bdVaJa')))

            # Gets links from specific page
            links2 = driver.find_elements_by_css_selector('.card-result-img .sc-bdVaJa')
            links2 = [link.get_attribute('href') for link in links2]

            print('Number of urls scraped at page' + current_page.text + ':' + str(len(links2)))

            # Appends new links to links object
            links.extend(links2)

    driver.close()
# Note: To run the app from VSCode select lines up until driver.close() If you select until one line BELOW driver.close() the app wont open.
# In other words the app wont run if your cursor is standing on an empty line below the actual code.

len(links)
with open('house_links.txt','w') as fp:
    json.dump(links,fp)