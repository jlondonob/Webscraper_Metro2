from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait #para esperar a que pagina cargue JavaScript
from selenium.webdriver.common.keys import Keys #para escribir en la pagina
from selenium.webdriver.chrome.options import Options # add headless option to driver

url = 'https://www.metrocuadrado.com/casas/arriendo/medellin/'
driver_path = '/Users/puchu/Desktop/WebScraper_Metro2/chromedriver'

chrome_options = Options()
chrome_options.add_argument('--headless')

webdriver = webdriver.Chrome(
    executable_path=driver_path,
    #options=chrome_options
)

with webdriver as driver:
    
    # Open website stored in `url` object
    driver.get(url)  

    # Removes cookies banner that is blocking the next page button by clicking on accept
    accept_cookies_button = driver.find_element_by_css_selector('.disclamer-action a')
    accept_cookies_button.click()  

    # Locates next page button for further use.  Also creates an empty arrow_disabled object
    next_page_button = driver.find_element_by_css_selector('.item-icon-next a')
    arrow_disabled = driver.find_elements_by_css_selector('.item-icon-next.page-item.disabled')

    while True:
        if len(arrow_disabled) > 0:
            print('No more pages left')
            break
        else:
            # Only purpose of this chunk is testing. It may be deleted
            current_page=driver.find_element_by_css_selector('.page-item.active')
            print(int(current_page.text)+1) 
            # Clicks next page and checks if button is disabled
            next_page_button.click()
            arrow_disabled = driver.find_elements_by_css_selector('.item-icon-next.page-item.disabled')

    driver.close()
