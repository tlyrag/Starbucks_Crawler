import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import json

# Grab content from URL (Pegar conteúdo HTML a partir da URL)
menu_url = "https://www.starbucks.com/menu"

## Instancing Firefox Automation
option = Options()
option.headless = True


def getDrinkTypes(url):
    driver = webdriver.Firefox()
    driver.get(url)
    driver.implicitly_wait(10)  # in seconds
    starbucks_table = pd.DataFrame(columns = ['Drink Type','Drink Type Link','Coffee Name','Coffee Url','Ingredients'])
    ### Getting HTML Elements from Website
    element = driver.find_element(By.ID,"drinks")
    html_content = element.get_attribute('outerHTML')

    driver.quit()

    ### Reading Html Elements to grab Drink Type and Drink Type Url
    soup = BeautifulSoup(html_content, 'html.parser')
    print('Parsing Soup')
    drink_type = soup.find_all("span",class_="hiddenVisually")
    drink_type_list_soup = soup.find_all(class_='block linkOverlay__primary tile___1wb3i', href=True)
    drink_type_list =[]

    for drink in drink_type_list_soup:
        drink_type_list.append(drink['href'])

    #print(drink_type_list)


    ## Creating Dataframe
    df = pd.DataFrame(drink_type,columns=['Drink Type'])
    df['Drink Type Link'] = drink_type_list
    #print(df)

    #print(df['Drink Type Link'][0])
    #df.to_csv('dftocsv.csv')

    for drink in df.index:
        print('----------Iterating ------------')
        drink_type = (df['Drink Type'][drink])
        drink_link = (df['Drink Type Link'][drink])
        temp_table = getCofeeTypes(drink_link,drink_type)
        print(temp_table)
        starbucks_table = starbucks_table.append(temp_table) 
        starbucks_table.to_csv('starbucks.csv')
            

        driver.quit()

    
def getCofeeTypes(coffeeUrlEndpoint,drink_type):
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
        drink_type_list.append(drink_type)
        drink_type_url_list.append(coffeeUrlEndpoint)
        coffee_list.append(coffee.get_text())
        coffee_url_list.append(coffee['href'])
        #getting Drink info
        ingredient_list = getCoffeeRecipie(coffee['href'])
        coffee_ingredient_list.append(ingredient_list )
        
    #print(cofee_list)
    #print(cofee_url_list)
    data = {'Drink Type': drink_type_list, 'Drink Type Link' : drink_type_url_list, 'Coffee Url': coffee_url_list, 'Coffee Name' :coffee_list, 'Ingredients' : coffee_ingredient_list  }
    temp_table = pd.DataFrame(data)
    return temp_table

def getCoffeeRecipie(drink_url_endpoint):
    drink_url_base = 'https://www.starbucks.com'
    driver = webdriver.Firefox()
    driver.get(drink_url_base +  drink_url_endpoint)
    driver.implicitly_wait(2)  # in seconds
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
        return ingredient_list

getDrinkTypes(menu_url)