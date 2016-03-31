# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 22:33:42 2016

@author: HP-06
"""

import unicodedata
from bs4 import BeautifulSoup
import time
import requests
import csv
import re

##http://www.amazon.in/s/ref=nb_sb_ss_c_0_10?url=search-alias%3Dkitchen&field-keywords=handicraft&sprefix=handicraft%2Caps%2C342
##http://www.amazon.in/s/ref=sr_pg_2?rh=n%3A976442031%2Ck%3Ahandicraft&page=2&keywords=handicraft
##http://www.amazon.in/s/ref=sr_pg_400?rh=n%3A976442031%2Ck%3Ahandicraft&page=400&keywords=handicraft

gen_url2='http://www.amazon.in/s/ref=sr_pg_'
gen_url3='?rh=n%3A976442031%2Ck%3Ahandicraft&page='
gen_url4='&keywords=handicraft'

item_id=0
writer =  open('item_seller.csv', 'wb')
out = csv.writer(writer, delimiter=',')

data_out=['item_name','seller_page_url']

out.writerow(data_out)

##loop for pages


for i in range(400):
    print "page "+str(i+1)
     
    time.sleep(1)
    if (i+1)==1:
        ##extract from page1
        url= 'http://www.amazon.in/s/ref=nb_sb_ss_c_0_10?url=search-alias%3Dkitchen&field-keywords=handicraft&sprefix=handicraft%2Caps%2C342'
        ##page = urllib2.urlopen(url)
        r = requests.get("http://www.amazon.in/s/ref=nb_sb_ss_c_0_10?url=search-alias%3Dkitchen&field-keywords=handicraft&sprefix=handicraft%2Caps%2C342")
        soup = BeautifulSoup(r.content, 'html.parser')

        ##soup = BeautifulSoup(page.read(), 'html.parser')
        ul=soup.find_all(id="s-results-list-atf")
        ##each item on a page
        k=len(ul[0].contents)
        for j in range(k): ##each item                           
                item_id+=1
                ##print item_id
                li=ul[0].contents[j]
                
                divs=li.contents[0]

                text=li.get_text().encode('utf-8')
                by_index=text.find('by')
                item_name=text[:by_index]
                offers_index=text.find(' offers')
                if offers_index != -1:
                    ##rs_text=text[:offers_index]
                    seller_page_url=str(li.find("a",{"class":"a-size-small a-link-normal a-text-normal"}).get("href"))
                else:
                    seller_page_url=''
                
                
                
                
                ##seller_page_url=str(li.find("a",{"class":"a-size-small a-link-normal a-text-normal"}).get("href"))
                
                item_row=[item_name,seller_page_url]
                out.writerow(item_row)
                ##save above data in excel               
                                   

    else:
        ##extract from page2 nd all other
        j=i+1
        url= gen_url2+str(j)+gen_url3+str(j)+gen_url4
        ##page = urllib2.urlopen(url)
        ##soup = BeautifulSoup(page.read(), 'html.parser')
        r = requests.get(url)
        soup= BeautifulSoup(r.content, 'html.parser')
        ul=soup.find_all(id="s-results-list-atf")
        ##each item on a page
        k=len(ul[0].contents)
        for j in range(k): ##each item
                item_id+=1
                ##print item_id
                li=ul[0].contents[j]
                divs=li.contents[0]

                text=li.get_text().encode('utf-8')
                by_index=text.find('by')
                item_name=text[:by_index]
                offers_index=text.find(' offers')
                if offers_index != -1:
                    ##rs_text=text[:offers_index]
                    seller_page_url=str(li.find("a",{"class":"a-size-small a-link-normal a-text-normal"}).get("href"))
                else:
                    seller_page_url=''
                
                item_row=[item_name,seller_page_url]
                out.writerow(item_row)        
       
       
writer.close()


