#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import functools 
import os

#import the traceback error found in code
traceBack = open("traceBackTest.txt","r")

#read in the StackOverflow question database and drop all columns that are not needed
# for the text analysis (Tf-Idf)
queryResults = pd.read_csv('FinalQuestions.csv')
queryResults.drop(["Id", "AcceptedAnswerId"], axis = 1, inplace = True) 
queryResults = queryResults.dropna()

#create a similarity table, before we begin iterating through each row of questions,
# to collect each similarity score during each iteration
simTable = pd.DataFrame(columns = ["Cosine Similarity", "Index"])
 
# iterate through each row in the questions table to be able to 
# analyze each individual question
for index, row in queryResults.iterrows():
    # open a temporary file to write each question into
    # closing after opening will allow the temporary file 
    # to be written over with the next iteration. 
    qResults = open("testing0.txt", "w")
    qResults.write(row["Title"])
    qResults.close()
    
    #read in the question and compiler (traceback) message
    documentA = open("testing0.txt", "r+")
    documentA = documentA.read()
    documentB = traceBack
    documentB = traceBack.read()
    
    #create a bag of words by splitting the entire file by spaces
    bagOfWordsA = documentA.split(' ')
    bagOfWordsB = documentB.split(' ')
    
    #begin cleaning the documents for Tf-Idf
    uniqueWords = set(bagOfWordsA).union(set(bagOfWordsB))
    
    #bag of words to proccess the files given
    numOfWordsA = dict.fromkeys(uniqueWords,0)
    for word in bagOfWordsA:
        numOfWordsA[word] += 1
    numOfWordsB = dict.fromkeys(uniqueWords,0)
    for word in bagOfWordsB:
        numOfWordsB[word] += 1
    

    #removing stopwords
    stop_words = stopwords.words('english')
    processed_A = [w for w in bagOfWordsA if not w in stop_words] 
    processed_A = [] 
    processed_B = [w for w in bagOfWordsB if not w in stop_words]
    processed_B = []

    for w in bagOfWordsA: 
        if w not in stop_words: 
            processed_A.append(w)
    for w in bagOfWordsB: 
        if w not in stop_words: 
            processed_B.append(w)
    
# once the data has been cleaned proceed to create methods to compute term frequency
    def computeTF (wordDict, bagOfWords):
        tfDict = {}
        bagOfWordsCount = len(bagOfWords)
        for word, count in wordDict.items():
            tfDict[word] = count / float(bagOfWordsCount)
        return tfDict

    tfA = computeTF(numOfWordsA, processed_A)
    tfB = computeTF(numOfWordsB, processed_B)
# then another method to compute inverse document frequency 
    def computeIDF(documents):
        import math
        N = len(documents)
        idfDict = dict.fromkeys(documents[0].keys(), 0)
        for document in documents:
            for word, val in document.items():
                if val > 0:
                    idfDict[word] += 1
        for word, val in idfDict.items():
            idfDict[word] = math.log(N/float(val))
        return idfDict

    idfs = computeIDF([numOfWordsA, numOfWordsB])
# lastly a method to compute the combined tf-idf scores 
    def computeTFIDF(tfBagOfWords, idfs):
        tfidf = {}
        for word, val in tfBagOfWords.items():
            tfidf[word] = val * idfs[word]
        return tfidf
    tfidfA = computeTFIDF(tfA, idfs)
    tfidfB = computeTFIDF(tfB, idfs)
# place the tfidf scores into a dataframe in order to vectorize
    df = pd.DataFrame([tfidfA, tfidfB])
#vectorize the tfidf scores so they can be used to compute cosine 
# similarity 
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([documentA, documentB])
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns = feature_names)
    df = df.rename(index = {0 : 'documentA'})
    df = df.rename(index = {1: 'documentB'})

    # finish computing the similarity scores using linear_kernel
    from sklearn.metrics.pairwise import linear_kernel
    similarity = linear_kernel(vectors[0:1], vectors).flatten()
    #place cosine similarity scores as well as post id and the question being 
    # analyzed into a table for later computations.
    simTable = simTable.append({'Cosine Similarity' : similarity, "Question": queryResults.iloc[index], ""}, 
                               ignore_index = True)
    #export the table into a new file in order to manipulate in next method being used
simTable.to_csv('testing2.csv')


# In[ ]:




