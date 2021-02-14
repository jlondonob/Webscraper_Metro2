from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait #para esperar a que pagina cargue JavaScript
from selenium.webdriver.common.keys import Keys #para escribir en la pagina

url = 'https://www.metrocuadrado.com/casas/arriendo/medellin/'
driver_path = '/Users/puchu/Desktop/WebScraper_Metro2/chromedriver'

webdriver = webdriver.Chrome(
    executable_path=driver_path
)

#Tengo que entender bien que hace la funcion 'with'
with webdriver as driver:
    wait = WebDriverWait(driver, 10)
    driver.get(url)

    results = driver.find_elements_by_class_name('card-title')
    for name in results:
        print(name.text)
        print()
    driver.close()