import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from pathlib import Path
import json


drink_url = 'https://www.starbucks.com/menu/product/418/hot'
option = Options()
option.headless = True
driver = webdriver.Firefox()
driver.get(drink_url)
driver.implicitly_wait(5)  # in seconds
element = driver.find_element(By.CSS_SELECTOR,'#content > div.sb-global-gutters.sb-global-gutters--logoOffset.pt5 > div > div.lg-flex > div.flex-grow.column___1a8HI.columnRight___1GOba')
html_content = element.get_attribute('outerHTML')
driver.quit()
soup = BeautifulSoup(html_content, 'html.parser')


ingredients = soup.find_all('li')
# ingredients_types = soup.find_all(class_='floatLabel floatLabel--isActive cursor-pointer')
# ingridient_html = soup.find_all(class_='sb-fieldBase__childWrapper flex items-center')

# for ingredient_type in ingredients_types:
#     print(ingredient_type.get_text())
ingredient_list =[]
for ingredient in ingredients:
    ingredient_list.append(ingredient.get_text())


df = pd.DataFrame(ingredient_list)
print(df)





    

    