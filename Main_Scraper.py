from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait #para esperar a que pagina cargue JavaScript
from selenium.webdriver.common.keys import Keys #para escribir en la pagina
from selenium.webdriver.chrome.options import Options # add headless option to driver

url = 'https://www.metrocuadrado.com/casas/arriendo/medellin/'
driver_path = '/Users/puchu/Desktop/WebScraper_Metro2/chromedriver'

chrome_options = Options()
chrome_options.add_argument('--headless')

# This opens a chrome browser installed in 'dirvepath' with options specified
# in 'chrome_options object'
webdriver = webdriver.Chrome(
    executable_path=driver_path,
    options=chrome_options
)
# Sets number of pages that the scraper will analyze. In the future the script
# will detect this number automatically. Either through:
# 1. Condition to stop if cannot go further.
# 2. Scrapes number of pages located at bottom of webpage and uses as input.

number_pages = 10

# Open webdriver
with webdriver as driver:
    # If more than 10 seconds to load then close
    wait = WebDriverWait(driver, 10) 
    
    # Open website stored in `url` object
    driver.get(url)                  

    # Find all elements with class "sc=bdVaJA" inside calss "card-result-img"
    links = driver.find_elements_by_css_selector('.card-result-img .sc-bdVaJa')
    
    # Loop trhough all elements in list `links` and get the href attribute from each element
    links = [link.get_attribute('href') for link in links]

    # Close Webdriver
    driver.close()

# Show that links were correctly retrieved
links[0:5]
