import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from pathlib import Path
import json


drink_url = 'https://www.starbucks.com/menu/drinks/hot-coffees'
option = Options()
option.headless = True
driver = webdriver.Firefox()
driver.get(drink_url)
driver.implicitly_wait(5)  # in seconds
element = driver.find_element(By.CSS_SELECTOR,'#content > div.footerOutOfView___14U1r.contentWithSubnav___2OXSW > div > div')
html_content = element.get_attribute('outerHTML')
driver.quit()
soup = BeautifulSoup(html_content, 'html.parser')

cofees = soup.find_all(class_='block linkOverlay__primary prodTile')

cofee_list = []
cofee_url_list = []
for cofee in cofees:
    cofee_list.append(cofee.get_text())
    cofee_url_list.append(cofee['href'])
print(cofee_list)
print(cofee_url_list)
df = pd.DataFrame(cofee_list,columns=['Cofee Name'])
df['Cofee Url'] = cofee_url_list

print(df)


    

    