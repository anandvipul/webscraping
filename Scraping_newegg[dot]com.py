#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import time


# In[2]:


def cnumkk(complete_url):
    response = requests.get(complete_url)
    print(response)
    html_test = response.text
    soup_test = BeautifulSoup(html_test)
    
    return soup_test


def url_maker(search_term):
    base_url = 'https://www.newegg.com/'
    atr = 'p/pl?d='+search_term+'&Page='+str(1)
    complete_url = base_url + atr
    soup_test = cnumkk(complete_url)
    div_soup = soup_test.find_all('div', class_='btn-group-cell')
    count = 0
    while (len(div_soup) == 1 or len(div_soup) == 0) and count < 5:
        soup_test = cnumkk(complete_url)
        div_soup = soup_test.find_all('div', class_='btn-group-cell')
        count += 1
        time.sleep(2)
        del soup_test
        print('count',count, 'len(div_soup)', len(div_soup))
    try:
        int_no_high = int(div_soup[-2].text)
        print('tried')
    except:
        int_no_high = 1
        print('excepted')
    
    int_no_high = int(div_soup[-2].text)
    link_list = [] 
    for i in range(int_no_high):
        atr = 'p/pl?d='+search_term+'&Page='+str(i+1)
        complete_url = base_url + atr
        link_list.append(complete_url)
        
    return link_list, int_no_high


# In[3]:


input_name = input('Enter the item to search: ')
url_list, max_page = url_maker(input_name)
print('No. of pages to crawl is {}'.format(max_page))


# In[4]:


def extractor(html_soup):
    item_div = html_soup.find_all('a', class_="item-title", title="View Details")
#     item_name = item_div[0].text
#     list_item_name.append(item_name)
    promo = html_soup.find_all('p',class_="item-promo")
#     list_promo.append(promo[0].text)
    price = html_soup.find_all('li', class_="price-current")
#     price_item = float(price[0].strong.text) + float(price[0].sup.text)
#     list_price.append(price_item)
    return item_div, promo, price


# In[7]:


import progressbar
# Name of Item
list_item_name = []
# Promo if available
list_promo = []
# Price of the item
list_price = []

for i in progressbar.progressbar(range(max_page)):
    current_url = url_list[i]
    html_1 = requests.get(current_url).text
    html_soup = BeautifulSoup(html_1)
    item_div = html_soup.find_all('a', class_="item-title", title="View Details")
    item_div, promo, price = extractor(html_soup)
    for i in range(len(item_div)):
#         item_name, promo, price_item = extractor(html_soup)
#         list_item_name.append(item_div[i].text)
        try:
            list_item_name.append(item_div[i].text)
        except:
            list_item_name.append('N/A')
            
        #########################################
        try:
            list_promo.append(promo[i].text)
        except:
            list_promo.append('N/A')
        #############################################
        try:
            price_item ='$' + str(price[i].strong.text) + str(price[i].sup.text)
            list_price.append(price_item)
        except:
            list_price.append('N/A')


# In[8]:


import pandas as pd
test_df = pd.DataFrame({'Item Name': list_item_name,
'Comments': list_promo,
'Price': list_price,
})


# In[9]:


test_df.to_csv(input_name+'.csv')


# In[ ]:




