# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 16:39:49 2016

@author: HP-06
"""

"""
http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?p%5B%5D=sort%3Drelevance&sid=1m7&filterNone=true&start=106&q=handicraft&ajax=true&_=1458041263457

http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?p%5B%5D=sort%3Drelevance&sid=1m7&filterNone=true&start=91&q=handicraft&ajax=true&_=1458041088045

http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?p%5B%5D=sort%3Drelevance&sid=1m7&filterNone=true&start=121&q=handicraft&ajax=true&_=1458041386191

http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?p%5B%5D=sort%3Drelevance&sid=1m7&filterNone=true&start=241&q=handicraft&ajax=true

http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?p%5B%5D=sort%3Drelevance&sid=1m7&filterNone=true&start=1500&q=handicraft&ajax=true&_=1458045713153

http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?p%5B%5D=sort%3Drelevance&sid=1m7&filterNone=true&start=16&q=handicraft&ajax=true&_=1458109730971

"""

"""
import urllib2
content = urllib2.urlopen("http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?p%5B%5D=sort%3Drelevance&sid=1m7&filterNone=true&start=72932&q=handicraft&ajax=true\
").read()

print content

"""


import unicodedata
from bs4 import BeautifulSoup
import time
import requests
import csv
import re


url="http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?p%5B%5D=sort%3Drelevance&sid=1m7&filterNone=true&start=1&q=handicraft&ajax=true"

u1=url.find('start')
s1=url[:117]

u2=url.find('&q=handicraft')
s2=url[u2:]

item_id=0

writer =  open('f_item_detail.csv', 'wb')
out = csv.writer(writer, delimiter=',')

data_out=['item_id','item_name','url','no_reviews','rating']
out.writerow(data_out)

home="http://www.flipkart.com"

for i in range(100):
        time.sleep(5)
        print "page"+str(i+1)
        nurl=s1+str(1+i*15)+s2
        r = requests.get(nurl)
        soup = BeautifulSoup(r.content, 'html.parser')
        div=soup.find_all("div",{"class":"gd-col gu4"})
        k=len(div)
        for p in range(k):
            item_id+=1
            href=str(div[p].findAll("a",{"class":"fk-display-block"})[0].get('href'))
            curl=(home+href).encode('utf-8')
            name=div[p].findAll("a",{"class":"fk-display-block"})[0].get_text().encode('utf-8').strip()
            
            if not div[p].findAll('div',{'class':'pu-rating'}):
                rating="0 stars"
                no_reviews="0 rating"
            else:
                rating=div[p].findAll('div',{'class':'fk-stars-small'})[0].get('title').encode('utf-8')##substring
                no_reviews=div[p].findAll('div',{'class':'pu-rating'})[0].get_text().encode('utf-8').strip()
            
            data=[item_id,name,curl,no_reviews,rating]
            ##print data
            out.writerow(data)            

writer.close()       