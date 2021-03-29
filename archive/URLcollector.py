#--------------------------------------------------------------------------------------#
#-----------------------| SCRAPER SETUP |----------------------------------------------#
#--------------------------------------------------------------------------------------#

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait             #wait until javascript data loads
from selenium.webdriver.common.keys import Keys                     #simulate pressing keys or buttons in webpage
from selenium.webdriver.chrome.options import Options               #add headless option to driver
from selenium.webdriver.support import expected_conditions as EC    #used with webdriverwait to wait until a certain condition is met
from selenium.webdriver.common.by import By                         

import json                                                         #write list of urls as json file


#########################CURRENT STATUSS #################
#If assigned True only extracts urls from first page
Testing = False
###########################################################


# Set cities to scrape
cities = ['medellin']
types = ['casa', 'apartamento']

home_pages = []
base_url = 'https://www.metrocuadrado.com'

for city in cities:
    for type in types:
        home_page = [base_url + '/' + type + '/venta/' + city]
        home_pages.extend(home_page)

print (f"Currently scraping links for {types} in {cities}".format(types, cities))


driver_path = '/Users/puchu/Desktop/WebScraper_Metro2/chromedriver'

chrome_options = Options()
chrome_options.add_argument('--headless')

webdriver = webdriver.Chrome(
    executable_path=driver_path,
    options=chrome_options
)



with webdriver as driver:
    
    # Creates a web object that will be used later. It stores the following information
    # " This is a wait where the conection will time out if takes more than 10s to load"
    wait = WebDriverWait(driver, 10)

    links = []
    for i in range(len(home_pages)):
        # Open first homepage
        driver.get(home_pages[i])  

        # Removes cookies banner that's blocking the next page button by clicking on accept
        if i == 0:
            accept_cookies_button = driver.find_element_by_css_selector('.disclamer-action a')
            accept_cookies_button.click()  

    
        # Locates next page button for further use.  Also creates an empty arrow_disabled object
        next_page_button = driver.find_element_by_css_selector('.item-icon-next a')
        arrow_disabled = driver.find_elements_by_css_selector('.item-icon-next.page-item.disabled')

        links1 = driver.find_elements_by_css_selector('.card-result-img .sc-bdVaJa')
        links1 = [link.get_attribute('href') for link in links1]
        
        if Testing==False:
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
                    links1.extend(links2)
        else:
            print('Testing mode: ON')  
        links.extend(links1)
    driver.close()

with open('collectedURLS.txt','w') as fp:
    json.dump(links,fp)