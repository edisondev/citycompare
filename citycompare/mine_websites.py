# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 20:48:45 2017

@author: Nick
"""

from sodapy import Socrata
import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time
import pandas as pd


datasets=["calgary", "edmonton", "novascotia","winnipeg", "regina", "sfgov"]
ext=["ca","ca","ca","ca","ca","org"]
#client = Socrata("data.calgary.ca", None)
#client.get('atsy-3a4w')
datasets=["sfgov"]
for idx,city in enumerate(datasets):
    iSite=25
    keep_reading =True
    #city="calgary"
    #for city in datasets:
    print(city)
    while keep_reading==True: 
        #main_page = 'https://data.'+city+'.ca/browse?limitTo=datasets&page='+str(iSite)
        main_page = 'https://data.'+city+'.'+ext[idx]+'/browse?limitTo=datasets&page='+str(iSite)
        req = urllib2.Request(main_page, headers={'User-Agent' : "Magic Browser"}) 
        con = urllib2.urlopen( req )
        soup=BeautifulSoup(con.read(), 'html.parser')
        page_links=soup.find_all('meta', {'itemprop':'sameAs'})
        
        if(len(page_links==0)): #check that the 
            print("Found end")
            keep_reading=False
            break    
        
        with open(r'C:\Users\Nick\Desktop\city_database.csv', 'ab') as csvfile:
            citywriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar=' ', quoting=csv.QUOTE_MINIMAL)    
            for i in range(0,len(page_links)):
                citywriter.writerow([city+' ; '+ str(page_links[i]['content']) ] ) 
        iSite=iSite+1
        if iSite>50:
            keep_reading=False
        time.sleep(1) 
        print(iSite)

    #page_links[0]['content']