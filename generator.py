# Tomasz Kiełczewski
import random
import re

import requests
from bs4 import BeautifulSoup

# def save_html(html, path):
#     with open(path, 'wb') as f:
#         f.write(html)
#
#
# def open_html(path):
#     with open(path, 'rb') as f:
#         return f.read()
#
#
#
#
#
# save_html(response.content, 'someelectonicshop')
#
# html = open_html('someelectonicshop')

separator = "|"
separatorInRow = "^"

response = requests.get("https://www.someelectonicshop.pl")

html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')



#Strips string form all charaters apart from numbers and comma
def stripToNum(str):
    tmp = ''
    for i in range(0, len(str) - 1):
        # if int(str[i]) < 48 or int(str[i]) > 57:
        if str[i].isdigit() or str[i] == ',':
            tmp = tmp + str[i]
    return tmp


# Adds zero to one-numberd months or days for date format
def zeroPrefix(num):
    if len(str(num)) == 1:
        s = '0' + str(num)
    else:
        s = str(num)
    return s


uls = soup.select('nav ul nav.category-list ul li a')
catLinks = []
for row in uls:
    catLinks.append('https://www.someelectonicshop.pl' + row.get('href') + '?per_page=90')

categories = []
for row in uls:
    cat = row.text.strip()
    categories.append(cat)

# Select only categories:
i = -1
for cat in categories:
    i += 1
    if cat == 'Pokaż wszystkie':
        del categories[i]
        del catLinks[i]

# print(categories)
# print(catHrefs)

parentCategories = ['Laptopy i Tablety', 'Telefony i GPS', 'Komputery stacjonarne', 'Podzespoły komputerowe',
                        'Urządzenia peryferyjne', 'Gaming', 'Foto, TV i Audio', 'Oprogramowanie', 'Akcesoria']

parentCatId = 0
catFile = open('kategorie.csv', 'w')
catFile.write('Category ID;Active (0/1);Name *;Parent category;Root category (0/1);Description;Meta title;Meta keywords;Meta description;URL rewritten\n')
catFile.write(  '3;1;Laptopy i Tablety;Strona Główna;0;Super Laptopy i Tablety;Meta title-Laptopy i Tablety;Meta keywords-Laptopy i Tablety;Meta description-Laptopy i Tablety;Laptopy i Tablety\n'
              + '4;1;Telefony i GPS;Strona Główna;0;Super Telefony i GPS;Meta title-Telefony i GPS;Meta keywords-Telefony i GPS;Meta description-Telefony i GPS;Telefony i GPS\n'
              + '5;1;Komputery stacjonarne;Strona Główna;0;Super Komputery stacjionarne;Meta title-Komputery stacjionarne;Meta keywords-Komputery stacjionarne;Meta description-Komputery stacjionarne;Komputery stacjonarne\n'
              + '6;1;Podzespoły komputerowe;Strona Główna;0;Super Podzespoły komputerowe;Meta title-Podzespoły komputerowe;Meta keywords-Podzespoły komputerowe;Meta description-Podzespoły komputerowe;Podzespoły komputerowe\n'
              + '7;1;Urządzenia peryferyjne;Strona Główna;0;Super Urządzenia peryferyjne;Meta title-Urządzenia peryferyjne;Meta keywords-Urządzenia peryferyjne;Meta description-Urządzenia peryferyjne;Urządzenia peryferyjne\n'
              + '8;1;Gaming;Strona Główna;0;Super Gaming;Meta title-Gaming;Meta keywords-Gaming;Meta description-Gaming;Gaming\n'
              + '9;1;Foto, TV i Audio;Strona Główna;0;Super Foto, TV i Audio;Meta title-Foto, TV i Audio;Meta keywords-Foto, TV i Audio;Meta description-Foto, TV i Audio;Foto, TV i Audio\n'
              + '10;1;Oprogramowanie;Strona Główna;0;Super Oprogramowanie;Meta title-Oprogramowanie;Meta keywords-Oprogramowanie;Meta description-Oprogramowanie;Oprogramowanie\n'
              + '11;1;Akcesoria;Strona Główna;0;Super Akcesoria;Meta title-Akcesoria;Meta keywords-Akcesoria;Meta description-Akcesoria;Akcesoria\n')


def addCategory(idx, nameCat, parentCatId):
    catFile.write(str(idx) + ';1;' + nameCat + ';' + parentCategories[parentCatId] + ';0;' + nameCat + ';' + nameCat + ';' + nameCat + ';' + nameCat + ';' + nameCat + '\n')




file = open('produkty.csv', 'w')
file.write('ID' + separator + 'Nazwa *' + separator + 'Marka' + separator + 'Kategorie (x,y,z...)' + separator + 'Cena (netto)' + separator + 'Cena (brutto)' + separator + 'Wysokość' + separator + 'Głębokość' + separator + 'Szerokość' + separator + 'Waga' + separator + 'Ilość' + separator + 'Ostatnie sztuki (1/0)' + separator + 'Opis' + separator + 'Obraz URL' + separator + 'Data wytworzenia produktu\n')
id = 0

nextCat = 0
catId = 11
flashFlag = 0
i = -1
for cat in categories:
    catId += 1
    parentCatId = nextCat
    addCategory(catId, cat, parentCatId)
    i += 1
    response = requests.get(catLinks[i])
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    # list of products:
    # products = soup.find_all(class_="sc-4el5v8-10 gLoboN sc-673ayz-0 dfQSis")
    products = soup.find_all(class_="sc-4ttund-0 kWNYsq")
    prodid = -1
    # dla 30 było 2369 produktow
    for row in products:
        prodid += 1

        if cat != 'Laptopy/Notebooki/Ultrabooki':
            if prodid > 12:
                break
        else:
            if prodid > 35:
                break
        response = requests.get('https://www.someelectonicshop.pl' + row.get('href'))
        html_doc = response.text
        soup = BeautifulSoup(html_doc, 'html.parser')

        # Opis:
        container = soup.find(id="mobileNavigation").next_sibling.next_sibling
        #container = soup.find(class_='product-description content product-page') #za krotki opis :/
        description = str(container.find(class_='row text-center')) + str(
            container.find(class_='row text-left')) + str(container.find(class_='text-left')) + str(
            container.find(class_='text-center'))
        if description == 'NoneNoneNoneNone' or description == 'NoneNoneNone' or description == 'NoneNone' or description == 'None':
            container = soup.find(class_='product-description content product-page')
            description = str(container)
        # description = str(container.find(class_='row text-center'))
        descriptionSoup = BeautifulSoup(description, 'html.parser')
        scripts = descriptionSoup.select('script')
        for script in scripts:
            description = description.replace(str(script), '')
        inputs = descriptionSoup.select('input')
        for inp in inputs:
            description = description.replace(str(inp), '')
        description = description.replace('\t', '')
        description = description.replace('\n', '')
        description = description.replace('\r', '')
        description = description.replace('|', '/')
        # clearer = re.compile(r'\s+')
        # description = clearer.sub('', description)
        if description == 'None':
            description = ''
        # Specyfikacja:
        specs = soup.find(class_='sc-1re71we-27 dahrJY sc-1vidtud-0 fgCLKi')
        height = ''
        width = ''
        depth = ''
        weight = ''
        # ;Wysokość;Głębokość;Szerokość;Waga;
        if specs is not None:
            params = specs.select('div div div div div div div div')
            for param in params:
                if param.text == 'Wysokość':
                    height = params[params.index(param) + 1].text
                    height = stripToNum(height)
                if param.text == 'Szerokość':
                    width = params[params.index(param) + 1].text
                    width = stripToNum(width)
                if param.text == 'Głębokość':
                    depth = params[params.index(param) + 1].text
                    depth = stripToNum(depth)
                if param.text == 'Waga':
                    weight = params[params.index(param) + 1].text
                    weight = stripToNum(weight)

        # print([height, width, depth, weight])
        # Zdjęcia:
        photos = soup.find_all(class_="sc-1tblmgq-0 sc-1y93ua6-0 dajIfQ sc-1tblmgq-2 ebGOQj")
        photosLinks = []
        for photo in photos:
            photosLinks.append(photo.select_one('img').get('src'))
        urls = separatorInRow.join(photosLinks)
        # Nazwa, marka, cena
        container = soup.find(id="mobileNavigation").next_sibling.next_sibling
        name = container.div['data-product-name']
        price = container.div['data-product-price']
        brand = container.div['data-product-brand']
        amount = random.randint(1, 200)
        if amount < 10:
            last = str(1)
        else:
            last = str(0)
        amount = str(amount)
        id += 1
        priceNetto = str(round(float(price) / 1.23, 2))
        print(name)
        # Date:
        date = ''
        if (id % 6) == 0:
            day = random.randint(1, 9)
            date = '2020-01-' + zeroPrefix(day)
        else:
            year = random.randint(2017, 2019)
            month = random.randint(1, 12)
            if month == 2:
                day = random.randint(1, 28)
            elif month < 8:
                if (month % 2) == 1:
                    day = random.randint(1, 31)
                if (month % 2) == 0:
                    day = random.randint(1, 30)
            else:
                if (month % 2) == 0:
                    day = random.randint(1, 31)
                if (month % 2) == 1:
                    day = random.randint(1, 30)

            date = str(year) + '-' + zeroPrefix(month) + '-' + zeroPrefix(day)
        # 'ID;Nazwa *;Marka;Kategorie (x,y,z...);Cena (netto);Cena (brutto);Wysokość;Głębokość;Szerokość;Waga;Ilość;Ostatnie sztuki (1/0);Opis;Obraz URL; Data\n'
        text = (str(id) + separator + name + separator + brand + separator + cat + separatorInRow + parentCategories[parentCatId] + separator + priceNetto + separator + price + separator + height + separator + depth + separator + width + separator + weight + separator + amount + separator + last + separator + description + separator + urls + separator + date + '\n')
        file.write(text)
    if cat == 'Akcesoria do tabletów':
        nextCat += 1
    elif cat == 'Akcesoria do dronów':
        nextCat += 1
    elif cat == 'Akcesoria do monitorów':
        nextCat += 1
    elif cat == 'Karty video':
        nextCat += 1
    elif cat == 'Tablety graficzne':
        nextCat += 1
    elif cat == 'Fotele dla graczy':
        nextCat += 1
    elif cat == 'Pamięci flash':
        if flashFlag == 1:
            nextCat += 1
            flashFlag += 1
        elif flashFlag == 0:
            flashFlag += 1
    elif cat == 'Kontrola rodzicielska':
        nextCat += 1
file.close()
catFile.close

#Pobierz product-description content product-page i usun skrypt!!

#Test just for 1 soundbar.
# response = open('soundbar.html', 'r')
# # html_doc = response.text
# soup = BeautifulSoup(response, 'html.parser')
#
# response = requests.get("https://www.someelectonicshop.pl/p/523166-notebook-laptop-156-hp-pavilion-gaming-i5-8300h-16gb-256-1050ti.html")
# #file = open("lenovoLegion.html", 'w')
#
# html_doc = response.text
# soup = BeautifulSoup(html_doc, 'html.parser')
#
# #file.write(html_doc)
# #file.close()
# id = 0
# # Opis:
# container = soup.find(id="mobileNavigation").next_sibling.next_sibling
# #container = soup.find(class_='product-description content product-page') #za krotki opis :/
# description = str(container.find(class_='row text-center')) + str(
#     container.find(class_='row text-left')) + str(container.find(class_='text-left')) + str(
#     container.find(class_='text-center'))
# if description == 'NoneNoneNoneNone' or description == 'NoneNoneNone' or description == 'NoneNone' or description == 'None':
#     container = soup.find(class_='product-description content product-page')
#     description = str(container)
# #description = str(container.find(class_='product-description content product-page'))
# descriptionSoup = BeautifulSoup(description, 'html.parser')
# scripts = descriptionSoup.select('script')
# for script in scripts:
#     description = description.replace(str(script), '')
# description = description.replace('\t', '')
# description = description.replace('\n', '')
# description = description.replace('\r', '')
# # clearer = re.compile(r'\s+')
# # description = clearer.sub('', description)
# if description == 'None':
#     description = ''
# # Specyfikacja:
# specs = soup.find(class_='sc-1re71we-27 dahrJY sc-1vidtud-0 fgCLKi')
# #Spec sc-1vidtud-1 eQseYH
# height = ''
# width = ''
# depth = ''
# weight = ''
#
# # ;Wysokość;Głębokość;Szerokość;Waga;
# if specs is not None:
#     params = specs.select('div div div div div div div div')
#     for param in params:
#         if param.text == 'Wysokość':
#             height = params[params.index(param) + 1].text
#             height = stripToNum(height)
#         if param.text == 'Szerokość':
#             width = params[params.index(param) + 1].text
#             width = stripToNum(width)
#         if param.text == 'Głębokość':
#             depth = params[params.index(param) + 1].text
#             depth = stripToNum(depth)
#         if param.text == 'Waga':
#             weight = params[params.index(param) + 1].text
#             weight = stripToNum(weight)
#
# # print([height, width, depth, weight])
# # Zdjęcia:
# photos = soup.find_all(class_="sc-854dbh-0 ojv8fg-1 oLNXW sc-854dbh-2 sYtzT")
# photosLinks = []
# for photo in photos:
#     photosLinks.append(photo.select_one('img').get('src'))
# urls = separatorInRow.join(photosLinks)
# # Nazwa, marka, cena
# container = soup.find(id="mobileNavigation").next_sibling.next_sibling
# name = container.div['data-product-name']
# price = container.div['data-product-price']
# brand = container.div['data-product-brand']
#
# amount = random.randint(1, 200)
# if amount < 10:
#     last = str(1)
# else:
#     last = str(0)
# amount = str(amount)
# id += 1
# priceNetto = str(round(float(price) / 1.23, 2))
# print(name)
# # Date:
# date = ''
# if (id % 6) == 0:
#     day = random.randint(1, 9)
#     date = '2020-01-' + zeroPrefix(day);
# else:
#     year = random.randint(2017, 2019)
#     month = random.randint(1, 12)
#     if month == 2:
#         day = random.randint(1, 28)
#     elif month < 8:
#         if (month % 2) == 1:
#             day = random.randint(1, 31)
#         if (month % 2) == 0:
#             day = random.randint(1, 30)
#     else:
#         if (month % 2) == 0:
#             day = random.randint(1, 31)
#         if (month % 2) == 1:
#             day = random.randint(1, 30)
#
#     date = str(year) + '-' + zeroPrefix(month) + '-' + zeroPrefix(day)