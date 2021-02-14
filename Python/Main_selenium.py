from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait #para esperar a que pagina cargue JavaScript
from selenium.webdriver.common.keys import Keys #para escribir en la pagina

# usados para esperar a que aparezcan contenedores de casas
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.by import By

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