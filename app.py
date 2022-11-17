import scrapper_controller_2 as scp

# Grab content from URL (Pegar conteúdo HTML a partir da URL)
menu_url = "https://www.starbucks.com/menu"

starbucks = scp.getDrinkTypes(menu_url)
starbucks.to_csv('Starbucks.csv')

for drink in starbucks.index:
    print('----------Iterating:{} of {} ------------'.format(drink,len(starbucks)))
    drink_type = (starbucks['Drink Type'][drink])
    drink_link = (starbucks['Drink Type Link'][drink])
    try:
        temp_table = scp.getCofeeTypes(drink_link,drink_type)
        print(temp_table)
        starbucks = starbucks.append(temp_table) 
        starbucks.to_csv('Starbucks.csv')
    except:
        print('Failed to grab {} information'.format(starbucks['Drink Type'][drink]))
        starbucks = starbucks.append(temp_table) 
        starbucks.to_csv('Starbucks.csv')

