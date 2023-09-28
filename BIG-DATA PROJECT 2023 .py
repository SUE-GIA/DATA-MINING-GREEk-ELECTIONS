#!/usr/bin/env python
# coding: utf-8

# In[4]:


#Big Data Project 2023
get_ipython().system('pip install tweepy==3.10.0')


# In[28]:


import tweepy
#import time
import pandas as pd
import re
import matplotlib.pyplot as plt
plt.style.use('ggplot')


# In[29]:


#set API keys
API_KEY ="0ehInzmh7rVILZZUyzGEyj3p3"
API_KEY_SECRET ="ywdUlYSxiHgYAlUb4KqEg97LdPjRQrRk0QMWNdTls1WcIWo6Iy"
OAUTH_TOKEN ="18873874-kwkRjbIz3DdKRuLYqdepf1o1eJjpamXQEO0NTySVb"
OAUTH_TOKEN_SECRET ="s0z47tZNaKGMQSJLroBLgZpi8xuw7k1nCRrUC7dm7H0M1"

#authentication
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=5)
api = tweepy.API(auth)


# In[30]:


#Parameters for selecting tweets
hashtag = '#εκλογες2023'
query = tweepy.Cursor(api.search, q=hashtag, lang="el", since="2023-01-05", encoding="utf8").items (500)
tweets = [{'Tweets' :tweet.text, 'Timestamp' : tweet.created_at} for tweet in query]
tweets


# In[31]:


#Creation of Data Frame
df = pd.DataFrame.from_dict(tweets)
df.head(499)


# In[32]:


df.info


# In[33]:


#Refrencing 
Mitsotakis_refs = [ 'Μητσοτάκης', 'Κυριάκος', 'Κυριάκος Μητσοτάκης', 'Κ. Μητσοτάκης','Κ. Μητσοτάκη', 'Μητσοτάκη','#Μητσοτάκης', 'ΝΔ', 'Νέα Δημοκρατία', 'ΝΕΑ ΔΗΜΟΚΡΑΤΙΑ', '#ΝΔ', 'Μητσοτακης', 'Κυριακος', 'Κυριακος Μητσοτακης','Μητσοτακη','#Μητσοτακης','#ΜΗΤΣΟΤΑΚΗΣ', 'Νεα Δημοκρατια', 'μητσοτακης', 'κυριακος', 'κυριακος μητσοτακης','μητσοτακη','#μητσοτάκης', 'νέα δημοκρατία', 'Kyriakos Mitsotakis', 'kmitsotakis', 'mitsotakis', 'Mitsotakis']
Tsipras_refs = [ 'Τσίπρας', 'Αλέξης', 'Αλέξης Τσίπρας', 'Α. Τσίπρας', 'Α. Τσίπρα', 'Αλέξη', 'Τσίπρα','#Τσίπρας', 'Σύριζα', 'ΣΥΡΙΖΑ', '#ΣΥΡΙΖΑ', '#Σύριζα','#ΤΣΙΠΡΑΣ' 'Τσιπρας', 'Αλεξης', 'Αλεξης Τσιπρας','Τσιπρα','#Τσιπρας', 'Συριζα','#Συριζα', 'τσιπρας', 'αλεξης', 'αλεξης τσιπρας','τσιπρα','#τσιπρας', 'συριζα', '#συριζα', 'Alexis Tsipras', 'atsipras', 'tsipras', 'Tsipras']
Androulakis_refs=['Νίκος Ανδρουλάκης','Ν. Ανδρουλάκης', 'Ν. Ανδρουλάκη', 'Ανδρουλάκης', 'Ανδρουλάκη', 'ΠΑΣΟΚ', 'πασοκ', '#ΠΑΣΟΚ', '#PASOK' 'Ανδρουλάκης Νίκος', 'Ανδρουλακης Νικος', 'Νικος Ανδρουλάκης', '#ΑΝΔΡΟΥΛΑΚΗΣ', 'Πανελλήνιο Σοσιαλιστικό Κίνημα', 'πανελληνιο σοσιαλιστικο κινημα', 'ανδρουλακης', 'νικος ανδρουλαλης', 'Nikos Androulakis', 'androulakisnick', 'androulakis', 'Androulakis', '#pasok', '#πασοκ']
Koutsoumpas_refs=['Δημήτρης Κουτσούμπας', 'Δημήτρη Κουτσούμπα', 'Δ. Κουτσούμπας', 'Δ. Κουτσούμπα', 'Κουτσούμπας', 'Κουτσούμπα', 'ΚΚΕ', 'κκε', '#ΚΚΕ', '#KKE', 'Δημητρης Κουτσουμπας', 'Δημητρη Κουτσουμπα', 'Δ. Κουτσουμπας', 'Δ. Κουτσουμπα', 'Κουτσουμπας', 'Κουτσουμπα', 'KOUTSOUMPAS', 'KOUTSOUBAS', 'dkoutsoumpas', 'Koutsoumpas', 'Κομμουνιστικό Κόμμα Ελλάδας', '#κκε', 'κουτσουμπας']


# In[34]:


#flagging the tweets based on the subject
def subject(tweet, refs):
    flag = 0 
    for ref in refs:
        if tweet.find(ref) != -1:
            flag = 1
    return flag

df['Μητσοτάκης'] = df['Tweets'].apply(lambda x: subject(x, Mitsotakis_refs)) 
df['Τσίπρας'] = df['Tweets'].apply(lambda x: subject(x, Tsipras_refs))
df['Ανδρουλάκης'] = df['Tweets'].apply(lambda x: subject(x, Androulakis_refs))
df['Κουτσούμπας'] = df['Tweets'].apply(lambda x: subject(x, Koutsoumpas_refs))
df.head(30)


# In[35]:


#Cleaning the Tweets
def cleanText(txt):
    txt = re.sub(r'@[A-Za-z0-9]+','', txt)
    txt = re.sub(r'[A-Za-z]+','', txt)
    txt = re.sub(r'RT[\s]+','', txt)
    txt = re.sub(r'[^\w]', ' ', txt)
    txt = re.sub(r':','', txt)
    txt = re.sub(r'#','', txt)
    txt = re.sub(r'_','', txt)
    txt = re.sub(r'{','', txt)
    txt = re.sub(r'}','', txt)
    txt = re.sub(r'\u20AC', '', txt)
    txt = re.sub(r'["u"\U0001F600-\U0001F64F"]+', '', txt)
    txt = re.sub(r'["u"\U0001F300-\U0001F5FF"]+', '', txt)
    txt = re.sub(r'["u"\U0001F680-\U0001F6FF"]+', '', txt)
    txt = re.sub(r'["u"\U0001F1E0-\U0001F1FF"]+', '', txt)
    txt = re.sub(r'[\n]+','', txt)
    
   
    return txt


# In[36]:


df['Clean Tweets']=df['Tweets'].apply(cleanText) 
df.head(499)


# In[37]:


results=df.dtypes
results


# In[38]:


#Tried getting polarity and sensivity from spaCy and other libs for greek tweets ...

#import spacy
#nlp = spacy.load('el_core_news_sm')
#from spacytextblob.spacytextblob import SpacyTextBlob
#nlp.add_pipe("spacytextblob")

      

#def polarity_tweets(tweet):
 #   doc = nlp(tweet)
  #  polarity = doc._.polarity
   # return polarity
#def subjectivity_tweets(tweet):
  #  doc = nlp(tweet)
   # subjectivity = doc._.subjectivity
   # return subjectivity
    
    
#df['Polarity']= df['Clean Tweets'].apply(polarity_tweets)
#df['Subjectivity']= df['Clean Tweets'].apply(subjectivity_tweets)
#df.head(499)


# In[39]:


#Getting the results of the flags
ND_df=df[df['Μητσοτάκης']==1]
len(ND_df)


# In[40]:


ND_df


# In[41]:


SYR_df=df[df['Τσίπρας']==1]
len(SYR_df)


# In[42]:


SYR_df


# In[43]:


PASOK_df=df[df['Ανδρουλάκης']==1]
len(PASOK_df)


# In[44]:


PASOK_df


# In[45]:


KKE_df=df[df['Κουτσούμπας']==1]
len(KKE_df)


# In[46]:


KKE_df


# In[47]:


ALL_df=df[(df['Τσίπρας']==1) & (df['Μητσοτάκης']==1) & (df['Μητσοτάκης']==1) & (df['Ανδρουλάκης']==1) & (df['Κουτσούμπας']==1)]
len(ALL_df)


# In[48]:


ALL_df


# In[49]:


#USING MATPLOT/ GENERATING GRAPHS
counts = df[['Μητσοτάκης', 'Τσίπρας', 'Ανδρουλάκης', 'Κουτσούμπας']].apply(pd.Series.value_counts)


# In[50]:


labels = ['Μητσοτάκης', 'Τσίπρας', 'Ανδρουλάκης', 'Κουτσούμπας', 'Όλοι']
Μητσοτάκης = counts.loc[1, 'Μητσοτάκης']
Τσίπρας = counts.loc[1, 'Τσίπρας']
Ανδρουλάκης = counts.loc[1, 'Ανδρουλάκης']
Κουτσούμπας = counts.loc[1, 'Κουτσούμπας']
Όλοι = ((df['Μητσοτάκης'] & df['Τσίπρας'] & df['Ανδρουλάκης'] & df['Κουτσούμπας']).sum())


# In[51]:


values = [Μητσοτάκης, Τσίπρας, Ανδρουλάκης, Κουτσούμπας, Όλοι]
colors = ["blue", "yellow", "green", "red", "black"]


# In[52]:


plt.bar(labels, values, color=colors)
plt.xlabel('Presidents of political Parties')
plt.ylabel('Frequency')
plt.title('Mentions of political parties/ presidents of said parties in tweets of the 500 tweet pool')
plt.show()


# In[53]:


plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%')
plt.title('Mentions of political parties/ presidents of said parties in tweets of the 500 tweet pool')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.show()


# In[54]:


x = range(5)
y = [Μητσοτάκης, Τσίπρας, Ανδρουλάκης, Κουτσούμπας, Όλοι]

# Plotting the function graph
plt.plot(x, y, marker='o', linestyle='-', color='blue')
plt.xticks(x, labels)
plt.xlabel('Presidents of political Parties')
plt.ylabel('Frequency')
plt.title('Mentions of political parties/ presidents of said parties in tweets of the 500 tweet pool')
plt.grid(True)
plt.show()


# In[55]:


#end


# In[ ]:




