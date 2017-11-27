# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 10:02:09 2017

@author: Nick
"""
import csv
import urllib2
from bs4 import BeautifulSoup
import re
import pandas as pd
import dateutil.parser as dparser


#Laods the data
def load_link(linkToPage, databaseType):
    print(databaseType)

#Use the following to find title without |Open Calagary Data
def longestSubstringFinder(string1, string2):
    answer = ""
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        match = ""
        for j in range(len2):
            if (i + j < len1 and string1[i + j] == string2[j]):
                match += string2[j]
            else:
                if (len(match) > len(answer)): answer = match
                match = ""
    return answer

    
# example to test the city_data
if __name__=='__main__':
    print('Test')
    pickleFilePath=r'C:\Users\Nick\Dropbox\Work\Data Science\14 - City Compare\GlobalDatabase.pkl'
    csvOutFilePath=r'C:\Users\Nick\Dropbox\Work\Data Science\14 - City Compare\GlobalDatabase.csv'
    csvFilePath='C:\Users\Nick\Desktop\city_database.csv'
    column_names=['database_title',
                               'city',
                               'views',
                               'downloads',
                               'last_updated',
                               'download_link',
                               'description']
    df = pd.DataFrame(columns=column_names)
    idx=0
    with open(csvFilePath) as csvfile:
        fileReader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in fileReader:
            print ', '.join(row)            
            try:            
                req = urllib2.Request(row[1], headers={'User-Agent' : "Magic Browser"}) 
                con = urllib2.urlopen( req )
                soup=BeautifulSoup(con.read(), "html.parser")
                
                #Get Parameters
                description=soup.find('meta', {'name':'description'})['content']
                description=description.encode('utf-8').strip()
                viewCount=re.findall('"viewCount":\d+',str(soup))
                viewCount=int(filter(str.isdigit,viewCount[0]))
                title=str(soup.find('title').text)
                lastUpdated=str(re.findall('[Uu]pdatedAt":.+?(?=")', str(soup))[0])
                lastUpdated=dparser.parse(lastUpdated,fuzzy=True)
                downloadCount=re.findall('"downloadCount":\d+',str(soup))
                downloadCount=int(filter(str.isdigit,downloadCount[0]))
                
                #Add to dataframe
                data=pd.DataFrame([[longestSubstringFinder(title,description),
                                   row[0],
                                   viewCount,
                                   downloadCount,
                                   pd.to_datetime(lastUpdated),
                                   row[1],
                                   description.replace('\n', ' ').replace('\r', '') ]],
                                   columns=column_names)
            except:
                print("Could not read")
                
            if len(df)==0:
                df=data
            else:
                df=df.append(data, ignore_index=True)
            idx=idx+1
            
            #if idx>5:
            #    break
            
            if idx % 10==0:
                df.to_pickle(pickleFilePath)  # where to save it, usually as a .pkl
                df.to_csv(csvOutFilePath,sep=';')
                
    df.to_pickle(pickleFilePath)  # where to save it, usually as a .pkl

    
    