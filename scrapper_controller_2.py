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
    try:
        driver = webdriver.Chrome()
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
        print('Finish Parsing')
        for drink in drink_type_list_soup:
            drink_type_list.append(drink['href'])
        
        ## Creating Dataframe
        df = pd.DataFrame(drink_type,columns=['Drink Type'])
        df['Drink Type Link'] = drink_type_list
        return df
    except: 
        print('Could not connect with Starbucks Menu Website')

    
def getCofeeTypes(coffeeUrlEndpoint,drink_type):
    #print(starbucks_table)
    coffeeUrl = 'https://www.starbucks.com' + coffeeUrlEndpoint
    try:
        print('Grabing {} Data in {}'.format(drink_type,coffeeUrlEndpoint))
        driver = webdriver.Chrome()
        driver.get(coffeeUrl)
        driver.implicitly_wait(5)  # in seconds
        element = driver.find_element(By.CSS_SELECTOR,'#content > div.footerOutOfView___14U1r.contentWithSubnav___2OXSW > div > div')
        html_content = element.get_attribute('outerHTML')
        driver.quit()
    except:
        print('Failed to grab Coffee Type information')
        data = {'Drink Type': drink_type_list, 'Drink Type Link' : drink_type_url_list, 'Coffee Url': coffee_url_list, 'Coffee Name' :coffee_list, 'Ingredients' : coffee_ingredient_list  }
        temp_table = pd.DataFrame(data)
        return temp_table

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
        # ingredient_list = getCoffeeRecipie(coffee['href'])
        #coffee_ingredient_list.append(ingredient_list )
        
    #print(cofee_list)
    #print(cofee_url_list)
    data = {'Drink Type': drink_type_list, 'Drink Type Link' : drink_type_url_list, 'Coffee Url': coffee_url_list, 'Coffee Name' :coffee_list, 'Ingredients' : coffee_ingredient_list  }
    temp_table = pd.DataFrame(data)
    return temp_table

def getCoffeeRecipie(drink_url_endpoint):
    try:
        ingredient_list =[]
        drink_url_base = 'https://www.starbucks.com'
        driver = webdriver.Firefox()
        driver.get(drink_url_base +  drink_url_endpoint)
        driver.implicitly_wait(2)  # in seconds
        element = driver.find_element(By.CSS_SELECTOR,'#content > div.sb-global-gutters.sb-global-gutters--logoOffset.pt5 > div > div.lg-flex > div.flex-grow.column___1a8HI.columnRight___1GOba')
        html_content = element.get_attribute('outerHTML')
        driver.quit()
        soup = BeautifulSoup(html_content, 'html.parser')
        ingredients = soup.find_all('li')
        
        for ingredient in ingredients:
            ingredient_list.append(ingredient.get_text())
            return ingredient_list
    except:
        print('Failed to grab {} ingredients'.format())
        ingredient_list.append('Unable to get data')
        return ingredient_list
