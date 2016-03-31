# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 03:14:18 2016

@author: HP-06
"""

import unicodedata
from bs4 import BeautifulSoup
import time
import requests
import csv
import re



f=open('f_item_detail.csv', 'rb')
reader=csv.reader(f)


writer2 = open('f_seller_detail.csv', 'wb')
out2 = csv.writer(writer2, delimiter=',')

data_out2=['item_id','cost','no_sellers']
out2.writerow(data_out2)


writer3 = open('f_extra_seller_detail.csv', 'wb')
out3 = csv.writer(writer3, delimiter=',')

data_out3=['item_id','seller_name','seller_rating']
out3.writerow(data_out3)


k=0
for r in reader:
    print k
    time.sleep(4)
    if k==0:
        k+=1
        continue
    item_id=r[0]
    item_url=r[2]
    k+=1      
    r=requests.get(item_url)
    soup = BeautifulSoup(r.content, "html5lib")
    
    c=soup.find_all('span',{'class':'selling-price omniture-field'})
    
    if not soup.find_all('span',{'class':'selling-price omniture-field'}):
        cost="Unknown"
    else:
        cost=soup.find_all('span',{'class':'selling-price omniture-field'})[0].get_text().encode('utf-8')
    
   
   
   
    seller_name_2=soup.find_all('a',{'class':'seller-name'})
    if not seller_name_2:
        seller_name_1="Not Available"
    else:
        seller_name_1=seller_name_2[0].get_text().encode('utf-8')
    
    seller_rating_2=soup.find_all('div',{'class':'seller-badge omniture-field'})
    if not seller_rating_2:
        seller_rating_1='Not Available'
    else:
        seller_rating_1=seller_rating_2[0].find('span').get_text().strip().encode('utf-8')
        
    ##soup.find_all('div',{'class':'seller-badge omniture-field'})[0].find('span').get_text().strip().encode('utf-8')

  
   
    seller_list=soup.find_all('a',{'class':'seller-name fk-inline-display'})
    xtra_seller=len(seller_list)  
    
    rate_list=soup.find_all('div',{'class':'rating-info-wrap'})
    
    if xtra_seller==0:
        no_seller=1
        seller=[item_id,seller_name_1,seller_rating_1]
        out3.writerow(seller)
    else:
        no_seller=xtra_seller
        for i in range(xtra_seller):
            name=seller_list[i].get_text().encode('utf-8')
            rate=rate_list[i].find_all('span',{'class':'fk-inline-block'})[0].get_text().encode('utf-8')
            seller=[item_id,name,rate]
            out3.writerow(seller)
            
    shop=[item_id,cost,no_seller]
    out2.writerow(shop)
        
                            
        
writer2.close()
writer3.close()

"""
soup.find_all("div",{"class":"fk-stars"})['title'] ##html5lib
s.find_all('span',{'class':'selling-price omniture-field'})

"""




