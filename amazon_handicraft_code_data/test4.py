# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 23:13:10 2016

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

f=open('item_seller.csv', 'rb')
reader=csv.reader(f)

##data_out=['item_id','seller_page_url']

writer2 = open('seller_detail.csv', 'wb')
out2 = csv.writer(writer2, delimiter=',')

data_out2=['item_name','seller_name','seller_rating','no_reviews']

out2.writerow(data_out2)


##http://www.amazon.in/gp/offer-listing/B01738H3K6/ref=sr_1_4_olp?s=kitchen&ie=UTF8&qid=1457715447&sr=1-4&keywords=handicraft&condition=new
##loop for pages

k=0
for r in reader:
    print k
    time.sleep(1)
    if k==0:
        k+=1
        continue
    item_name=r[0]
    ##print item_name
    k+=1  
    
    if r[1]!='':             
             first_url=r[1]
             r = requests.get(first_url)
             soup1 = BeautifulSoup(r.content, 'html.parser')
             content=soup1.find_all("div",{"class":"a-column a-span2 olpSellerColumn"})                    
             for i in content:
                            ##out2.write('%d;' % item_id)
                            shop_name=str(i.find('h3').get_text())[2:-2]
                            if not shop_name:
                                shop_name=i.find('h3').find('img')['alt'].encode('utf-8')
                            ##print shop_name
                            ##out2.write('%s;' % shop_name)
                            ##print shop_name
                            shop_rate_list=i.find('p').findAll("span",{"class":"a-icon-alt"})
    
                            text=i.get_text().encode('utf-8')
                            total_rating=0
                            tr=text.find(' total ratings')
                            if tr != -1:
                                total_rating=re.findall('\d+',text[0:tr])[-1]
                                                        
                            if not shop_rate_list:
                                shop_rating="0"
                            else:
                                shop_rating=str(i.find('p').findAll("span",{"class":"a-icon-alt"})[0].get_text())
                            ##out2.write('%s;' % shop_rating)
                            ##out2.write('\n')
                            ##print shop_rating
                            shop=[item_name,shop_name,shop_rating,total_rating]
                            out2.writerow(shop)
    else:
        shop_name=''
        shop_rating=''
        total_rating=''
        shop=[item_name,shop_name,shop_rating,total_rating]
        out2.writerow(shop)
        
                            
        
writer2.close()


