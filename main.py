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
    print(df)


    for drink in df:
        print(drink)['Drink Type Link']
        getCofeeTypes(drink['Drink Type Link'])
        

    driver.quit()

    
def getCofeeTypes(coffeeUrlEndpoint):
    coffeeUrl = 'https://www.starbucks.com' + coffeeUrlEndpoint
    driver = webdriver.Firefox()
    driver.get(coffeeUrl)
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

getDrinkTypes(menu_url)