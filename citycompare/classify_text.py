# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 18:18:33 2017

@author: Nick
"""
import six.moves.cPickle as pickle
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import time
import pandas as pd
import numpy as np
from scipy import spatial
import os

from matplotlib import pyplot as plt


NUM_TOPICS=200
PATH='C:\Users\Nick\Dropbox\Work\Data Science\14 - City Compare\citycompare\citycompare'

def initiate_pipline():
    tokenizer = RegexpTokenizer(r'\w+') #Words Separator
    en_stop = get_stop_words('en') # create English stop words list
    p_stemmer = PorterStemmer() # Create p_stemmer of class PorterStemmer
    
    pipeline = {'tokenizer':tokenizer,
                'stop_words': en_stop,
                'stemmer': p_stemmer}
    return pipeline
    
def return_tokens(pipeline, text):
    # clean and tokenize document string
    #TODO: remove numbers from string
    #TODO: remove unicode characters from string
    
    raw = text.lower()
    tokens = pipeline['tokenizer'].tokenize(raw)
    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in pipeline['stop_words']]
    # stem tokens
    #stemmed_tokens = [pipeline['stemmer'].stem(i) for i in stopped_tokens]
    #return stemmed_tokens
    return stopped_tokens

def generate_word2vec_corpus():
    filename=r'C:\Users\Nick\Dropbox\Work\Data Science\14 - City Compare\glove6B\glove.6B.200d.txt'
    model=gensim.models.KeyedVectors.load_word2vec_format(filename, binary=False)
    return model

def get_word2vec_vector_txt(model,pipeline, text):
    tokens=return_tokens(pipeline, text)
    doc_vector=np.zeros([1,model.vector_size], dtype=np.float32)
    for kToken in tokens:
        try:
            doc_vector=doc_vector+model[kToken]
        except:
            k=1
            #do nothing
    return doc_vector
    
def get_word2vec_vector_tkns(model,pipeline, tokens):
    doc_vector=np.zeros([1,model.vector_size], dtype=np.float32)
    for kToken in tokens:
        try:
            doc_vector=doc_vector+model[kToken]
        except:
            #do nothing
    return doc_vector
    
def compare_2_vectors(model, pipeline, text1, text2):
    tokens1=return_tokens(pipeline, text1)
    tokens2=return_tokens(pipeline, text2)
    if (len(tokens1)<10) | (len(tokens2)<10):
        return 0.0
        
    if len(tokens1)>len(tokens2):
        tokens1=tokens1[0:len(tokens2)]
    else:
        tokens2=tokens2[0:len(tokens1)]
    
    dv1=get_word2vec_vector_tkns(model,pipeline, tokens1)
    dv2=get_word2vec_vector_tkns(model,pipeline, tokens2)
    return (1-spatial.distance.cosine(dv1, dv2))
    
#compare_2_vectors(model, 
#                  pipeline, 
#                  cityDataset['description'][0],
#                  cityDataset['description'][7])


#Generate LDA corpus
def generate_LDA_corpus():
    print("Generate Corpus")
    pipeline=initiate_pipline()     
    trainDocuments=[]
    t=time.time()
    
    #Load the random wikipedia articles:
#    wiki_list=pickle.load(open(r"C:\Users\h192456\Desktop\backup for me\wiki_listv2.pkl",'rb'))   
#    # loop through document list        
#    for i in wiki_list:  
#        # add tokens to list
#        trainDocuments.append(return_tokens(pipeline, i ))
#    
#    del wiki_list
    
    #Load city Database descriptions
    path=r'C:\Users\Nick\Dropbox\Work\Data Science\14 - City Compare\citycompare\citycompare\GlobalDatabase.csv'
    cityDataset=pd.read_csv(path, 
                            sep=';',
                            encoding='utf-8')
    for i in cityDataset['description']:  
        # add tokens to list
        trainDocuments.append(return_tokens(pipeline, i ))
    
    #Create an LDA topic model
    pipeline['dictionary'] = corpora.Dictionary(trainDocuments)
    pipeline['corpus'] = [pipeline['dictionary'].doc2bow(text) for text in trainDocuments]    
    ldamodel = gensim.models.ldamodel.LdaModel(pipeline['corpus'], 
                                               num_topics=NUM_TOPICS, 
                                               id2word = pipeline['dictionary'],
                                               update_every=1,
                                               chunksize=1000,
                                               passes=5,
                                               random_state=1234)
    print(time.time()-t)
    print(len(trainDocuments))
    pickle.dump(pipeline,
                open(r'C:\Users\Nick\Dropbox\Work\Data Science\14 - City Compare\citycompare\citycompare\pipeline2.pkl', 'wb'), 
                protocol=2)
    return ldamodel,pipeline

def classify_text(lda,pipeline,newDocument):
    #Turn string into individual tokens:
    stemmedToken=return_tokens(pipeline,newDocument)
    
    #Turn tokens to bag-of-words:
    bagOfWords=pipeline['dictionary'].doc2bow(stemmedToken)
    topicList = lda[bagOfWords]
    return(topicList)
    
#Return maximum index and maximum values
def find_max(sparseArray):
    maxIndex=0
    for index in range(1,len(sparseArray)):
        if sparseArray[index][1]>sparseArray[maxIndex][1]:
            maxIndex=index
    return sparseArray[maxIndex][0], sparseArray[maxIndex][1]

#returns numpy array from sparse array
def sparse2array(sparseArray):
    outArray=np.zeros([NUM_TOPICS])
    for index in range(0, len(sparseArray)):
        outArray[sparseArray[index][0]]=sparseArray[index][1]
    return outArray

def parseTopicMatrix(topicMatrix, cityDataset, threshold=250):
    column_names=['City1',
                  'url1',
                  'index2',
                  'Description1',
                  'Description2',
                  'City2',
                  'index2',
                  'url2']
    df = pd.DataFrame(columns=column_names)
    for kMainTopic in range(0,topicMatrix.shape[0]):
        for kSideTopic in range(0,topicMatrix.shape[1]):
            if topicMatrix[kMainTopic][kSideTopic]>threshold:
                if cityDataset['city'][kMainTopic] !=cityDataset['city'][kSideTopic]:
                    print(topicMatrix[kMainTopic][kSideTopic],kMainTopic,kSideTopic)
                    data=pd.DataFrame([[cityDataset['city'][kMainTopic],
                                        cityDataset['download_link'][kMainTopic],
                                        kMainTopic,
                                        cityDataset['description'][kMainTopic].encode('ascii','ignore').decode('unicode_escape'),
                                        cityDataset['description'][kSideTopic].encode('ascii','ignore').decode('unicode_escape'),
                                        cityDataset['city'][kSideTopic],
                                        kSideTopic,
                                        cityDataset['download_link'][kSideTopic]]],
                                        columns=column_names)
                    #print(data)
                    df=df.append(data,ignore_index=True)
                
    df.to_html(os.path.join(r'C:\Users\Nick\Dropbox\Work\Data Science\14 - City Compare\citycompare\citycompare',
                            r'matchedDatasets_200.html'))
    return df


def print_specific_lines(k,num=0):
    print(k['City1'][num])
    print(k['Description1'][num])
    print(" ")
    print(k['City2'][num])
    print(k['Description2'][num])
    
    
def load_pickle_file():
    lda=pickle.load(open(r'C:\Users\Nick\Dropbox\Work\Data Science\14 - City Compare\citycompare\citycompare\lda2.pkl','rb'))
    pipeline=pickle.load(open(r'C:\Users\Nick\Dropbox\Work\Data Science\14 - City Compare\citycompare\citycompare\pipeline.pkl','rb'))
    topicMatrix=np.genfromtxt(r'C:\Users\Nick\Dropbox\Work\Data Science\14 - City Compare\citycompare\citycompare\topicMatrix.csv', 
                                     delimiter=',',
                                     dtype=np.uint8)
    path=r'C:\Users\Nick\Dropbox\Work\Data Science\14 - City Compare\citycompare\citycompare\GlobalDatabase.csv'
    cityDataset=pd.read_csv(path, 
                            sep=';',
                            encoding='utf-8')
    
    return lda, pipeline , topicMatrix  , cityDataset   

# example to test the city_data
if __name__=='__main__':
    #Load files
    pd.set_option('display.max_colwidth', -1)   
    lda=pickle.load(open(r'C:\Users\Nick\Dropbox\Work\Data Science\14 - City Compare\citycompare\citycompare\lda2.pkl','rb'))
    pipeline=pickle.load(open(r'C:\Users\Nick\Dropbox\Work\Data Science\14 - City Compare\citycompare\citycompare\pipeline.pkl','rb'))
    
    path=r'C:\Users\Nick\Dropbox\Work\Data Science\14 - City Compare\citycompare\citycompare\GlobalDatabase.csv'
    cityDataset=pd.read_csv(path, 
                            sep=';',
                            encoding='utf-8')
    
    #LDA
    #pp=initiate_pipline()
    topicMatrix=np.zeros([len(cityDataset),len(cityDataset)],
                          dtype=np.uint8)
    
    t=time.time()
    for kMainIndex in range(0,len(cityDataset)):
        mainTopics=classify_text(lda, 
                                pipeline,
                                cityDataset['description'][kMainIndex])
        mainTopicsVector=sparse2array(mainTopics)
        print(kMainIndex, time.time()-t)
        np.savetxt(r"topicMatrix.csv",
                   topicMatrix, 
                   fmt='%3d',
                   delimiter=',')
        for kSideIndex in range (0,len(cityDataset)):
            if kSideIndex == kMainIndex:
                continue
            sideTopics=classify_text(lda, 
                                     pipeline,
                                     cityDataset['description'][kSideIndex])
            sideTopicsVector=sparse2array(sideTopics)
            
            #calcualte cosine similarity
            spatial.distance.cosine(mainTopicsVector, 
                                    sideTopicsVector)
            #cosSim=np.dot(mainTopicsVector,sideTopicsVector)/(np.linalg.norm(mainTopicsVector)*np.linalg.norm(sideTopicsVector))
            cosSim=1-spatial.distance.cosine(mainTopicsVector, sideTopicsVector)
            topicMatrix[kMainIndex][kSideIndex]=np.uint8(255*cosSim)
    
    print(time.time()-t)
    
    plt.imshow(topicMatrix, interpolation='nearest')
    plt.show()
    
    
    #Word2Vec
    #Word2Vec
    #model=generate_word2vec_corpus()
    t=time.time()
    for kMainIndex in range(0,len(cityDataset)):
        if (kMainIndex%50)==0:
            print(kMainIndex, time.time()-t)
#            np.savetxt(r'C:\Users\Nick\Dropbox\Work\Data Science\14 - City Compare\citycompare\citycompare\topicMatrix_wv_200.csv',
#                       topicMatrix, 
#                       fmt='%3d',
#                       delimiter=',')
        for kSideIndex in range (0,len(cityDataset)):
            if kSideIndex == kMainIndex:
                continue
            cosSim=compare_2_vectors(model,
                                     pipeline, 
                                     cityDataset['description'][kMainIndex], 
                                     cityDataset['description'][kSideIndex])
            #calcualte cosine similarity
            topicMatrix[kMainIndex][kSideIndex]=np.uint8(255*cosSim)
#            if cosSim>0.97:
#                #print(kMainIndex)
#                print(cityDataset['description'][kMainIndex])
#                print(kSideIndex)
#                print(cityDataset['description'][kSideIndex])
#                print(cosSim)
#                print("\n")
    
    print(time.time()-t)
    
    plt.imshow(topicMatrix, interpolation='nearest')
    plt.show()
    
    
    #Laod the word2vec file
    path=r'C:\Users\Nick\Dropbox\Work\Data Science\14 - City Compare\citycompare\citycompare\topicMatrix_wv_200.csv'
    topicMatrix=np.loadtxt(path, 
                           dtype=np.uint8,
                           delimiter=',')
    df_small=parseTopicMatrix(topicMatrix,cityDataset,242)
    
    #Get topic of 2 files
    print('Test')
    #Dev Notes:
    #Need to take the same number of words from both datasets (truncate to shortest one?)