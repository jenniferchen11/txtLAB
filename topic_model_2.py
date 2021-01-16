import re
import numpy as np
import pandas as pd
from pprint import pprint
import os
import shutil
import csv
from csv import writer
import sys
import pickle
import random
from sklearn.utils import resample

#Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim import models
from gensim.models import LdaModel, CoherenceModel
from gensim.models.wrappers import LdaMallet

# Enable logging for gensim - optional
# import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

# spacy for lemmatization
import spacy

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

# 1. NLTK Stop words to remove unimportant vocabulary
import nltk
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
    
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

print("~grabbing data")
words_of_chunks = []
directory = r'txtLAB/topic_modeling/NYT_FanFic_Chunked_Combined'
for filename in os.listdir(directory):
    try:
        f = open(directory + os.sep + filename, 'r')
        raw_data = f.read()
        one_file_list = [1]
        one_file_list[0] = raw_data
        words_of_chunks.append(one_file_list)
    except:
        continue

print("~~data collected")
print("~~~~~~data size: " + str(len(words_of_chunks)))
print("~converting sentences to words")
data_words = list(sent_to_words(words_of_chunks))
# print(data_words)
print("~~done")

# 2. Build the bigram and trigram models
print("~building bigram / trigram models")
bigram = gensim.models.Phrases(data_words, min_count=5, threshold=75) # higher threshold fewer phrases.
trigram = gensim.models.Phrases(bigram[data_words], threshold=75)  

print("~~done")
# Faster way to get a sentence clubbed as a trigram/bigram
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)

# See trigram example
# print(trigram_mod[bigram_mod[data_words[0]]])

print("~creating function remove_stopwords")
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

print("~creating function make_bigrams")
def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

print("~creating function make_trigrams")
def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

print("~~creating lemmatization function")
def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    #https://spacy.io/api/annotation
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

# 3. Removing stop words
print("~removing stopwords from data")
data_words_nostops = remove_stopwords(data_words)

# 4. Form Bigrams
print("~~making bigrams")
data_words_bigrams = make_bigrams(data_words_nostops)

# 5. Initialize spacy 'en' model, keeping only tagger component (for efficiency)
# python3 -m spacy download en
nlp = spacy.load('en', disable=['parser', 'ner'])

# 6. Do lemmatization keeping only noun, adj, vb, adv
print("~lemmatizing")
data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

# print(data_lemmatized[1])

# 7. Get Dictionary from pre-existing source
print("~~getting dictionary")
dict_words = []
#FIXED
#Original
#New: topic-modelling/FanFic_NYT_Dictionary.csv
dictionary_raw = 'txtLAB/topic_modeling/NYT_FanFic_Queer_Dic.csv'
with open(dictionary_raw) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        dict_words.append(str(row[0]))

dict_words = [d.split() for d in dict_words]
id2word = corpora.Dictionary(dict_words)
#print(id2word)

# 8. Create Corpus
print("~creating corpus")
texts = data_lemmatized
#print(texts)

# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]

#pprint(lda_model.print_topics())
print("~~starting LDA mallet")


#-------------------------------------------CREATING OUTPUT FILES------------------------------------------------

#---------K = 40---------
# Download File: http://mallet.cs.umass.edu/dist/mallet-2.0.8.zip

mallet_path = 'txtLAB/topic_modeling/mallet-2.0.8/bin/mallet'
lda_mallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=40, id2word=id2word, optimize_interval=20, iterations=1000, random_seed=2)

# Show Topics
# pprint(lda_mallet.show_topics(num_topics=-1, num_words=20, formatted=False)) # This is the correct one

# Term-topic matrix
tm_results = lda_mallet[corpus]
corpus_topics = [sorted(topics, key=lambda record: -record[1])[0] for topics in tm_results]
topics = [[(term, round(wt, 3)) for term, wt in lda_mallet.show_topic(n, topn=20)] for n in range(0, lda_mallet.num_topics)]
topics_df = pd.DataFrame([[term for term, wt in topic] for topic in topics], columns= ['Term '+str(i) for i in range(1,21)], index=['Topic '+str(t) for t in range(1,lda_mallet.num_topics+1)]).T
topics_df.to_csv("results_k40.csv")

# -------------K = 35----------
lda_mallet1 = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=35, id2word=id2word, optimize_interval=20, iterations=1000, random_seed=2)

# Term-topic matrix
tm_results1 = lda_mallet1[corpus]
corpus_topics1 = [sorted(topics, key=lambda record: -record[1])[0] for topics in tm_results1]
topics1 = [[(term, round(wt, 3)) for term, wt in lda_mallet1.show_topic(n, topn=20)] for n in range(0, lda_mallet1.num_topics)]
topics_df1 = pd.DataFrame([[term for term, wt in topic] for topic in topics1], columns= ['Term '+str(i) for i in range(1,21)], index=['Topic '+str(t) for t in range(1,lda_mallet1.num_topics+1)]).T
topics_df1.to_csv("results_k35.csv")

"""
print("making ONE csv for ALL the data lmao")
df_weights = pd.DataFrame.from_records([{v: k for v, k in row} for row in tm_results])
df_weights.columns = ['Topic ' + str(i) for i in range(1,41)]
df_weights.to_csv("~/Desktop/full_data_topic_probabilities.csv")
"""
##################################################################################################

def fanfic_portion(ldamallet = lda_mallet):

    print("~~~~~~~collecting fanfic subset data")
    words_of_chunks1 = []
    directory1 = r'txtLAB/topic_modeling/FanFic_Chunks'
    for filename in os.listdir(directory1):
        try:
            f = open(directory1 + os.sep + filename, 'r')
            raw_data = f.read()
            one_file_list = [1]
            one_file_list[0] = raw_data
            words_of_chunks1.append(one_file_list)
        except:
            continue

    print("~~data collected")
    print("~~~~~~data size: " + str(len(words_of_chunks1)))
    print("~converting sentences to words")
    data_words1 = list(sent_to_words(words_of_chunks1))
    # print(data_words)
    print("~~done")

    # Build the bigram and trigram models
    print("~building bigram / trigram models")
    bigram1 = gensim.models.Phrases(data_words1, min_count=5, threshold=75) # higher threshold fewer phrases
    trigram1 = gensim.models.Phrases(bigram[data_words1], threshold=75)  

    print("~~done")
    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod1 = gensim.models.phrases.Phraser(bigram1)
    trigram_mod1 = gensim.models.phrases.Phraser(trigram1)

    print("~creating function remove_stopwords")
    def remove_stopwords(texts):
        return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

    print("~creating function make_bigrams")
    def make_bigrams(texts):
        return [bigram_mod1[doc] for doc in texts]

    print("~creating function make_trigrams")
    def make_trigrams(texts):
        return [trigram_mod1[bigram_mod1[doc]] for doc in texts]

    print("~~creating lemmatization function")
    def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
        #https://spacy.io/api/annotation
        texts_out = []
        for sent in texts:
            doc = nlp(" ".join(sent)) 
            texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        return texts_out

    print("~removing stopwords from data")
    data_words_nostops1 = remove_stopwords(data_words1)

    # Form Bigrams
    print("~~making bigrams")
    data_words_bigrams1 = make_bigrams(data_words_nostops1)

    # Do lemmatization keeping only noun, adj, vb, adv
    print("~lemmatizing")
    data_lemmatized1 = lemmatization(data_words_bigrams1, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
    texts = data_lemmatized1
    #print(texts2)

    print("~~~lda mallet-ing the fanfic data")
    corpus2 = [id2word.doc2bow(text) for text in texts]
    tm_results = ldamallet[corpus2]

    print("making ONE csv for FF data")
    df_weights = pd.DataFrame.from_records([{v: k for v, k in row} for row in tm_results])
    df_weights.columns = ['Topic ' + str(i) for i in range(1,41)]
    df_weights.to_csv("~/Desktop/FanFic_topic_probabilities.csv")

fanfic_portion()

##################################################################################################

def nyt_portion(ldamallet = lda_mallet):

    print("~~~~~~~collecting fanfic subset data")
    words_of_chunks1 = []
    directory1 = r'txtLAB/topic_modeling/NYT_Chunked'
    for filename in os.listdir(directory1):
        try:
            f = open(directory1 + os.sep + filename, 'r')
            raw_data = f.read()
            one_file_list = [1]
            one_file_list[0] = raw_data
            words_of_chunks1.append(one_file_list)
        except:
            continue

    print("~~data collected")
    print("~~~~~~data size: " + str(len(words_of_chunks1)))
    print("~converting sentences to words")
    data_words1 = list(sent_to_words(words_of_chunks1))
    # print(data_words)
    print("~~done")

    # Build the bigram and trigram models
    print("~building bigram / trigram models")
    bigram1 = gensim.models.Phrases(data_words1, min_count=5, threshold=75) # higher threshold fewer phrases
    trigram1 = gensim.models.Phrases(bigram[data_words1], threshold=75)  

    print("~~done")
    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod1 = gensim.models.phrases.Phraser(bigram1)
    trigram_mod1 = gensim.models.phrases.Phraser(trigram1)

    print("~creating function remove_stopwords")
    def remove_stopwords(texts):
        return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

    print("~creating function make_bigrams")
    def make_bigrams(texts):
        return [bigram_mod1[doc] for doc in texts]

    print("~creating function make_trigrams")
    def make_trigrams(texts):
        return [trigram_mod1[bigram_mod1[doc]] for doc in texts]

    print("~~creating lemmatization function")
    def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
        #https://spacy.io/api/annotation
        texts_out = []
        for sent in texts:
            doc = nlp(" ".join(sent)) 
            texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        return texts_out

    print("~removing stopwords from data")
    data_words_nostops1 = remove_stopwords(data_words1)

    # Form Bigrams
    print("~~making bigrams")
    data_words_bigrams1 = make_bigrams(data_words_nostops1)

    # Do lemmatization keeping only noun, adj, vb, adv
    print("~lemmatizing")
    data_lemmatized1 = lemmatization(data_words_bigrams1, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
    texts = data_lemmatized1
    #print(texts2)

    print("~~~lda mallet-ing the fanfic data")
    corpus2 = [id2word.doc2bow(text) for text in texts]
    tm_results = ldamallet[corpus2]

    print("making ONE csv for FF data lmao")
    df_weights = pd.DataFrame.from_records([{v: k for v, k in row} for row in tm_results])
    df_weights.columns = ['Topic ' + str(i) for i in range(1,41)]
    df_weights.to_csv("~/Desktop/NYT_topic_probabilities.csv")

nyt_portion()