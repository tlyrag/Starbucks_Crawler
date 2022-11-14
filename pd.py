import pandas as pd
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import json

df = pd.read_csv('dftocsv.csv')
starbucks_table = pd.DataFrame(columns = ['Drink Type','Drink Type Link','Coffee Name','Coffee Url','Ingredients'])


def getCofeeTypes(coffeeUrlEndpoint):
    #print(starbucks_table)
    coffeeUrl = 'https://www.starbucks.com' + coffeeUrlEndpoint
    driver = webdriver.Firefox()
    driver.get(coffeeUrl)
    driver.implicitly_wait(5)  # in seconds
    element = driver.find_element(By.CSS_SELECTOR,'#content > div.footerOutOfView___14U1r.contentWithSubnav___2OXSW > div > div')
    html_content = element.get_attribute('outerHTML')
    driver.quit()
    soup = BeautifulSoup(html_content, 'html.parser')

    coffees = soup.find_all(class_='block linkOverlay__primary prodTile')

    coffee_list = []
    coffee_url_list = []
    drink_type_list = []
    drink_type_url_list = []
    coffee_ingredient_list =[]

    for coffee in coffees:
        drink_type_list.append('test')
        drink_type_url_list.append(coffeeUrlEndpoint)
        coffee_list.append(coffee.get_text())
        coffee_url_list.append(coffee['href'])
        coffee_ingredient_list.append('Ingredients')
        
    #print(cofee_list)
    #print(cofee_url_list)
    data = {'Drink Type': drink_type_list, 'Drink Type Link' : drink_type_url_list, 'Coffee Url': coffee_url_list, 'Coffee Name' :coffee_list, 'Ingredients' : coffee_ingredient_list  }
    temp_table = pd.DataFrame(data)
    return temp_table


#print(df)
for drink in df.iterrows():
    print(drink['Drink Type'])
    #print(drink['Drink Type URL'])
    #temp_table = getCofeeTypes(drink)
    #print(temp_table)
    #starbucks_table = starbucks_table.append(temp_table) 
    #starbucks_table.to_csv('starbucks.csv')
#     #df['value'] = 'test'
#     print('alow')
#     print(df[drink])

#print(df)
