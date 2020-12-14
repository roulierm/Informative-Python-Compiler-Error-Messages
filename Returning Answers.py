#!/usr/bin/env python
# coding: utf-8

# In[98]:


import pandas as pd

#open the data set that contains the cosine similarity scores
simResults = pd.read_csv('testing2.csv')

#clean up the file and name the unnamed file, correctly as PostId
results = simResults.rename( columns={'Unnamed: 0':'PostId'}, inplace=True )
results = simResults.drop(columns=['Index'])
results['Question'] = results['Question'].str.replace('Title', '')


# In[99]:


#group the dataframe by question or postId, either will work in this case
grouped_df = results.groupby("Question")
# from the grouped dataframe compute the maximum so we can see the highest similarity score
maximums = grouped_df.max()
maximums = maximums.reset_index()
maximums


# In[100]:


# to find the absolute maximum, find the head of the maximums list
maxi = maximums.head(1)


# In[101]:


#return the post id of the maximum from the dataframe
maxi = maxi['PostId']


# In[102]:


#open the questions dataframe so that we can return the 
#accepted answer id for the question with the highest similarity score
data = pd.read_csv("FinalQuestions.csv")


# In[96]:


#this will find the row in which the accepted answer id will be present
idNum = data.loc[data['Id'] == maxi]
#now the accepted answer id is stored in idNum
idNum = idNum['AcceptedAnswerId']
#open the answers data frame to match the accepted answer id this data frame
answers = pd.read_csv("FinalAnswers.csv")
finalAnswer = answers.loc[answers['Id'] = idNum]
#print the solution provided by stack overflow 
print(finalAnswer)

