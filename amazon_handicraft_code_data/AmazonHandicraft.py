# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 22:24:02 2016

@author: HP-06
"""

import urllib2
import unicodedata
from bs4 import BeautifulSoup


url= 'http://www.amazon.in/s/ref=nb_sb_ss_c_0_10?url=search-alias%3Dkitchen&field-keywords=handicraft&sprefix=handicraft%2Caps%2C485'
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read(), 'html.parser')

ul=soup.find_all(id="s-results-list-atf")

li=ul[0].contents[0]

divs=li.contents[0].contents

name=divs[2].contents

item_name=str(name[0].findAll("h2", { "class" : "a-size-base a-color-null s-inline s-access-title a-text-normal" })[0].get_text())

seller_name=str(name[1].get_text())

u_cost=divs[3].contents[0].findAll("a",{"class":"a-link-normal a-text-normal"})[0].get_text()

cost=unicodedata.normalize('NFKD', u_cost).encode('ascii','ignore')


u_seller=unicodedata.normalize('NFKD', divs[3].contents[3].get_text()).encode('ascii','ignore')

no_seller=u_seller[0:u_seller.find("from")]

no_customer_reviews=str(divs[5].findAll("a",{"class":"a-size-small a-link-normal a-text-normal"})[0].get_text())

product_rating=str(divs[5].findAll("span",{"class":"a-icon-alt"})[0].get_text())



url_seller=str(divs[3].contents[3].findAll("a",{"class":"a-size-small a-link-normal a-text-normal"})[0].get('href'))

item_page_url=str(name[0].findAll("a",{"class":"a-link-normal s-access-detail-page  a-text-normal"})[0].get('href'))


page1 = urllib2.urlopen(url_seller)
soup1 = BeautifulSoup(page1.read(), 'html.parser')

content=soup1.find_all("div",{"class":"a-column a-span2 olpSellerColumn"})


for i in content:
        shop_name=str(i.find('h3').get_text())[2:-2]
        print shop_name
        shop_rate_list=i.find('p').findAll("span",{"class":"a-icon-alt"})
        if not shop_rate_list:
            shop_rating="0"
        else:
            shop_rating=str(i.find('p').findAll("span",{"class":"a-icon-alt"})[0].get_text())
        print shop_rating


##for other pages 
last_page_no=str(soup1.findAll("ul",{"class":"a-pagination"})[0].findAll("li",{"class":"a-last"})[0].find_previous("li").get_text())
url_before_gp="http://www.amazon.in"
last_url=str(soup1.findAll("ul",{"class":"a-pagination"})[0].findAll("li",{"class":"a-last"})[0].find_previous("li").findAll("a")[0].get('href'))
index=last_url.rfind('=')
general_url=url_before_gp+last_url[0:index+1]
for i in range(last_page_no-1):
    if i!=0:
        url=general_url+str((i+1)*10)
        ##do the scrapping
        



 
   
       









