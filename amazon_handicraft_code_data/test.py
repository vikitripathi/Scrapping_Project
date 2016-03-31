# -*- coding: utf-8 -*-
"""
Created on Wed Mar 09 15:53:52 2016

@author: HP-06
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Mar 05 07:58:27 2016

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
writer =  open('item_detail.csv', 'wb')
out = csv.writer(writer, delimiter=',')


data_out=['item_id','item_name','seller_name','cost','no_seller','no_customer_reviews','product_rating']

out.writerow(data_out)


##loop for pages


for i in range(400):
    print "page "+str(i+1)
    
    time.sleep(4)
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
                print item_id
                li=ul[0].contents[j]
                
                divs=li.contents[0]

                text=li.get_text().encode('utf-8')
                by_index=text.find('by')
                item_name=text[:by_index]
                rs_index=text.find('\xc2\xa0\xc2\xa0')
                seller_name=text[by_index+3:rs_index]
                
                t=text.find('.00')
                cost=text[rs_index+4:t]

                offers_index=text.find(' offers')
                if offers_index != -1:
                    ##rs_text=text[:offers_index]
                    no_seller=int(re.findall('\d+',text[:offers_index])[-1])+1   
                else:
                    no_seller=1
                out_of_index=text.find('out of')
                if out_of_index != -1:
                    product_rating=re.findall('\d+\.\d+|\d+',text[:out_of_index])[-1]
                    no_customer_reviews=re.findall('\d+',text)[-1]
                else:
                    product_rating=0
                    no_customer_reviews=0
                    
                ##product_rating=divs[5].findAll("span",{"class":"a-icon-alt"})[0].get_text().encode('utf-8')
                ##out.write('%s;' % product_rating)
                
                item_row=[item_id,item_name,seller_name,cost,no_seller,no_customer_reviews,product_rating]
                out.writerow(item_row)
                ##save above data in excel
                """
                ##seller page 1
                url_seller=str(divs.findAll("a",{"class":"a-size-small a-link-normal a-text-normal"})[0].get('href'))
                ##page1 = urllib2.urlopen(url_seller)
                ##soup1 = BeautifulSoup(page1.read(), 'html.parser') 
                r = requests.get(url_seller)
                soup1 = BeautifulSoup(r.content, 'html.parser')
                content=soup1.find_all("div",{"class":"a-column a-span2 olpSellerColumn"})                    
                for i in content:
                        ##out2.write('%d;' % item_id)
                        shop_name=str(i.find('h3').get_text())[2:-2]
                        print shop_name
                        ##out2.write('%s;' % shop_name)
                        ##print shop_name
                        shop_rate_list=i.find('p').findAll("span",{"class":"a-icon-alt"})
                        
                        if not shop_rate_list:
                            shop_rating="0"
                        else:
                            shop_rating=str(i.find('p').findAll("span",{"class":"a-icon-alt"})[0].get_text())
                        ##out2.write('%s;' % shop_rating)
                        ##out2.write('\n')
                        ##print shop_rating
                        shop=[item_id,shop_name,shop_rate_list]
                        out2.writerow(shop)
                
                ##seller other pages
                last_page_no=str(soup1.findAll("ul",{"class":"a-pagination"})[0].findAll("li",{"class":"a-last"})[0].find_previous("li").get_text())
                url_before_gp="https://www.amazon.in"
                last_url=str(soup1.findAll("ul",{"class":"a-pagination"})[0].findAll("li",{"class":"a-last"})[0].find_previous("li").findAll("a")[0].get('href'))
                index=last_url.rfind('=')
                print last_url
                lu=last_url.split('?')
                
                str1="/ref=olp_page_"
                general_url=url_before_gp+lu[0]+str1
                general_url_2='?'+lu[1][0:index]
                print general_url+general_url_2
                for i in range(int(last_page_no)):
                    if i!=0:
                        url=general_url+str(i+1)+general_url_2+str((i)*10)
                        ##do the scrapping
                        ##page1 = urllib2.urlopen(url)
                        ##soup1 = BeautifulSoup(page1.read(), 'html.parser') 
                        r = requests.get(url)
                        soup1 = BeautifulSoup(r.content, 'html.parser')
                        content=soup1.find_all("div",{"class":"a-column a-span2 olpSellerColumn"})                    
                        for i in content:
                                ##out2.write('%d;' % item_id)
                                shop_name=str(i.find('h3').get_text())[2:-2]
                                ##out2.write('%s;' % shop_name)
                                ##print shop_name
                                shop_rate_list=i.find('p').findAll("span",{"class":"a-icon-alt"})
                                
                                if not shop_rate_list:
                                    shop_rating="0"
                                else:
                                    shop_rating=str(i.find('p').findAll("span",{"class":"a-icon-alt"})[0].get_text())
                                ##out2.write('%s;' % shop_rating)
                                ##out2.write('\n')
                                shop=[item_id,shop_name,shop_rate_list]
                                out2.writerow(shop)
                            ##print shop_rating 
                   """

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
                print item_id
                li=ul[0].contents[j]
                divs=li.contents[0].contents
                text=li.get_text().encode('utf-8')
                by_index=text.find('by')
                item_name=text[:by_index]
                rs_index=text.find('\xc2\xa0\xc2\xa0')
                seller_name=text[by_index+3:rs_index]
                t=text.find('.00')
                cost=text[rs_index+4:t]
                offers_index=text.find(' offers')
                if offers_index != -1:
                    no_seller=int(re.findall('\d+',text[:offers_index])[-1])+1
                else:
                    no_seller=1
                out_of_index=text.find('out of')
                if out_of_index != -1:
                    product_rating=re.findall('\d+\.\d+|\d+',text[:out_of_index])[-1]
                    no_customer_reviews=re.findall('\d+',text)[-1]
                else:
                    product_rating=0
                    no_customer_reviews=0
                    
                ##product_rating=divs[5].findAll("span",{"class":"a-icon-alt"})[0].get_text().encode('utf-8')
                ##out.write('%s;' % product_rating)
                
                item_row=[item_id,item_name,seller_name,cost,no_seller,no_customer_reviews,product_rating]
                out.writerow(item_row)
            
            
            
                ##save above data in excel
                """
                url_seller=str(divs[3].contents[3].findAll("a",{"class":"a-size-small a-link-normal a-text-normal"})[0].get('href'))
                ##page1 = urllib2.urlopen(url_seller)
                ##soup1 = BeautifulSoup(page1.read(), 'html.parser') 
                r = requests.get(url_seller)
                soup1 = BeautifulSoup(r.content, 'html.parser')
                content=soup1.find_all("div",{"class":"a-column a-span2 olpSellerColumn"})                    
                for i in content:
                        ##out2.write('%d;' % item_id)
                        shop_name=str(i.find('h3').get_text())[2:-2]
                        ##out2.write('%s;' % shop_name)
                        ##print shop_name
                        shop_rate_list=i.find('p').findAll("span",{"class":"a-icon-alt"})
                        
                        if not shop_rate_list:
                            shop_rating="0"
                        else:
                            shop_rating=str(i.find('p').findAll("span",{"class":"a-icon-alt"})[0].get_text())
                        ##out2.write('%s;' % shop_rating)
                        ##out2.write('\n')
                        ##print shop_rating
                        shop=[item_id,shop_name,shop_rate_list]
                        out2.writerow(shop)
                
                ##seller other pages
                last_page_no=str(soup1.findAll("ul",{"class":"a-pagination"})[0].findAll("li",{"class":"a-last"})[0].find_previous("li").get_text())
                url_before_gp="http://www.amazon.in"
                last_url=str(soup1.findAll("ul",{"class":"a-pagination"})[0].findAll("li",{"class":"a-last"})[0].find_previous("li").findAll("a")[0].get('href'))
                index=last_url.rfind('=')
                general_url=url_before_gp+last_url[0:index+1]
                for i in range(int(last_page_no)-1):
                    if i!=0:
                        url=general_url+str((i+1)*10)
                        ##do the scrapping
                        ##page1 = urllib2.urlopen(url)
                        ##soup1 = BeautifulSoup(page1.read(), 'html.parser') 
                        r = requests.get(url)
                        soup1 = BeautifulSoup(r.content, 'html.parser')
                        content=soup1.find_all("div",{"class":"a-column a-span2 olpSellerColumn"})                    
                        for i in content:
                                ##out2.write('%d;' % item_id)
                                shop_name=str(i.find('h3').get_text())[2:-2]
                                ##out2.write('%s;' % shop_name)
                                ##print shop_name
                                shop_rate_list=i.find('p').findAll("span",{"class":"a-icon-alt"})
                                
                                if not shop_rate_list:
                                    shop_rating="0"
                                else:
                                    shop_rating=str(i.find('p').findAll("span",{"class":"a-icon-alt"})[0].get_text())
                                ##out2.write('%s;' % shop_rating)
                                ##out2.write('\n')
                                shop=[item_id,shop_name,shop_rate_list]
                                out2.writerow(shop)  
                       
              """
       
       
writer.close()


