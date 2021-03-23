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

    wait = WebDriverWait(driver, 10)

    driver.get(url)  

    #accept cookies to remove banner
    accept_cookies_button = driver.find_element_by_css_selector('.disclamer-action a')
    accept_cookies_button.click()  

    #buttons
    min_area = driver.find_element_by_xpath("//div[label='Área (m²):']//div[@class='m2-select-container']")
    max_area = driver.find_element_by_xpath("(//div[label='Área (m²):']//div[@class='m2-select-container'])[2]")
    
    list_areas = ["60", "100", "200", "300", "400", "500", "1200"]
    areas_button = [f"//div[contains(text(), '{area} m')]" for area in list_areas]
    
    #loop through possible areas
    for i in range(0,6):
        min_area.click()
        driver.find_element_by_xpath(areas_button[i]).click()
        max_area.click()
        driver.find_element_by_xpath(areas_button[i+1]).click()

        #---
        #CODE TO GO TRHOUGH PAGES AND SCRAPE
        #---

        next_page_button = driver.find_element_by_css_selector('.item-icon-next a')
        arrow_disabled = driver.find_elements_by_css_selector('.item-icon-next.page-item.disabled')

        links1 = driver.find_elements_by_css_selector('.card-result-img .sc-bdVaJa')
        links1 = [link.get_attribute('href') for link in links1]

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

    driver.close()