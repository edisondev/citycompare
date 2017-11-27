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
    raw = text.lower()
    tokens = pipeline['tokenizer'].tokenize(raw)
    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in pipeline['stop_words']]
    # stem tokens
    stemmed_tokens = [pipeline['stemmer'].stem(i) for i in stopped_tokens]
    return stemmed_tokens

#Generate LDA corpus
def generate_LDA_corpus():
    print("Generated Corpus")
    #Load the random wikipedia articles:
    wiki_list=pickle.load(open(r"C:\Users\Nick\Dropbox\Work\Data Science\09 - quora question pairs\wiki_listv2.pkl", 'rb'))

    pipeline=initiate_pipline()    
    wiki_documents=[]
    t=time.time()
    # loop through document list        
    for i in wiki_list[0:100]:  
        # add tokens to list
        wiki_documents.append(return_tokens(pipeline, i ))
        
    #Create an LDA topic model
    dictionary = corpora.Dictionary(wiki_documents)
    corpus = [dictionary.doc2bow(text) for text in wiki_documents]    
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, 
                                               num_topics=5, 
                                               id2word = dictionary, 
                                               passes=1)
    print(time.time()-t)
    print(len(wiki_documents))

def classify_text(text1, text2):
    result=0
    print(result)

# example to test the city_data
if __name__=='__main__':
    print('Test')