#!/usr/bin/env python
# coding: utf-8
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import random
import re
import json
import pandas as pd
import numpy as np


url = 'https://www.formbot3d.com/products/voron-24-corexy-3d-printer-kit-with-different-print-sizes-for-choice'


# chrome_options = Options() 
# chrome_options.add_argument('--no-sandbox') 
# chrome_options.add_argument('--disable-dev-shm-usage')


# automatically use the correct chromedriver by using the webdrive-manager
path = ChromeDriverManager().install()


# initialize and close the driver (new): 
driver = webdriver.Chrome(path)

# initialize and close the driver (old): error SessionNotCreatedException
# driver = webdriver.Chrome(path)

# make sure that the page has time to properly open 
#time.sleep(3) 

driver.get(url)

assert 'Voron 2.4 CoreXY 3D Printer Kit with Different Print Sizes for Choice' == driver.title, 'Returned product name is different - {}'.format(X)

html = driver.page_source
driver.quit()


# html


soup = bs(html)
# soup


# check every product's stock level
def findAllNameIDpairs(s):
    dic = {}
    for i in s.find_all('div', class_=re.compile('btn_attr GoodBorderColor GoodBorderHoverColor')):
        dic[i.get('value')] = i.get('title')
    return dic


# check every product's stock level
def findAllStocks(s):
    for i in s.find_all('input', id=='ext_attr'):
        if re.search(r'\d{3}_\d{3}', i.get('value')):
            values = json.loads(i.get('value'))

    dic = findAllNameIDpairs(s)
    
    print_size = []
    hotend_type = []
    ships_from = []
    stocks = []
    for k, v in values.items():
        a, b, c = [dic[i] for i in k.split('_')]
        print_size.append(a)
        hotend_type.append(b)
        ships_from.append(c)
        stocks.append(v[1])
    
    return print_size, hotend_type, ships_from, stocks


print_size2, hotend_type2, ships_from2, stocks2 = findAllStocks(soup)


df2 = pd.DataFrame({'Print Size': print_size2, 
                    'Hotend Type': hotend_type2,
                    'Ships From': ships_from2,
                    'Stocks': stocks2})
#  df2.sort_values('Stocks', ascending=False).head()


print_sizes = list(set(print_size2))
hotend_types = list(set(hotend_type2))
ships_froms = list(set(ships_from2))


def findPrice(s):
    return s.find(class_='price themes_products_price').string


print_size = []
hotend_type = []
ships_from = []
price = []

# initialize and close the driver (new): 
driver = webdriver.Chrome(path)

# initialize and close the driver (old): error SessionNotCreatedException
# driver = webdriver.Chrome(path)

# make sure that the page has time to properly open 
#time.sleep(3) 

driver.get(url)

# check if it is the right product
assert 'Voron 2.4 CoreXY 3D Printer Kit with Different Print Sizes for Choice' == driver.title, 'Returned product name is different - {}'.format(X)

# click on buttons to get the specific product
for p in print_sizes:
    driver.find_element_by_xpath("//div[@title='{}']".format(p)).click()
    for h in hotend_types:
        driver.find_element_by_xpath("//div[@title='{}']".format(h)).click()
        for s in ships_froms:
            print_size.append(p)
            hotend_type.append(h)
            ships_from.append(s)
            driver.find_element_by_xpath("//div[@title='{}']".format(s)).click()
            # print('Scraping product -', (p, h, s))
            
            # scrape
            html = driver.page_source            
            price.append(findPrice(bs(html)))
            
            time.sleep(1)

driver.quit()

df = pd.DataFrame({'Print Size': print_size, 
                   'Hotend Type': hotend_type,
                   'Ships From': ships_from,
                   'Price': price})
# df.head()

final_df = pd.merge(left=df, right=df2, on = ['Print Size', 'Hotend Type', 'Ships From'])
final_df = final_df[final_df['Stocks']!='0'].sort_values(['Price', 'Stocks'], ascending=[True, False])


# with open("results.txt", "w") as f:
#    for i in final_df.columns:
#        f.write(str(i))
#        f.write(',')
#    f.write('\n')
#    np.savetxt(f, final_df.values, delimiter=',', fmt='%s')            

print(','.join(list(final_df.columns)))
for i in final_df.values:
    print(','.join(list(i)))