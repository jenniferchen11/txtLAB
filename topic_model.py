import re
import numpy as np
import pandas as pd
from pprint import pprint
import os
import shutil
import csv
import sys
import pickle

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim import models
from gensim.models import LdaModel, CoherenceModel
from gensim.models.wrappers import LdaMallet

# spacy for lemmatization
import spacy

# Enable logging for gensim - optional
# import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

# NLTK Stop words
import nltk
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
    
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

words_of_chunks = []
directory = r'txtLAB/topic_modeling/test_topic_model'
for filename in os.listdir(directory):
    f = open(directory + os.sep + filename, 'r')
    raw_data = f.read()
    one_file_list = [1]
    one_file_list[0] = raw_data
    words_of_chunks.append(one_file_list)

data_words = list(sent_to_words(words_of_chunks))
# print(data_words)

# Build the bigram and trigram models
bigram = gensim.models.Phrases(data_words, min_count=5, threshold=75) # higher threshold fewer phrases.
trigram = gensim.models.Phrases(bigram[data_words], threshold=75)  

# Faster way to get a sentence clubbed as a trigram/bigram
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)

# See trigram example
# print(trigram_mod[bigram_mod[data_words[0]]])

def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    #https://spacy.io/api/annotation
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

data_words_nostops = remove_stopwords(data_words)

# Form Bigrams
data_words_bigrams = make_bigrams(data_words_nostops)

# Initialize spacy 'en' model, keeping only tagger component (for efficiency)
# python3 -m spacy download en
nlp = spacy.load('en', disable=['parser', 'ner'])

# Do lemmatization keeping only noun, adj, vb, adv
data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

# print(data_lemmatized[1])

# Create Dictionary
dict_words = []
dictionary_raw = 'txtLAB/topic_modeling/FanFic_NYT_Dictionary.csv'
with open(dictionary_raw) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        dict_words.append(str(row[0]))

dict_words = [d.split() for d in dict_words]
id2word = corpora.Dictionary(dict_words)
#print(id2word)

# Create Corpus
texts = data_lemmatized

# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]

# print(corpus[0])
"""
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=20, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           eval_every=10,
                                           per_word_topics=True)
"""
#pprint(lda_model.print_topics())


# Download File: http://mallet.cs.umass.edu/dist/mallet-2.0.8.zip
mallet_path = 'txtLAB/topic_modeling/mallet-2.0.8/bin/mallet'
lda_mallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=20, id2word=id2word, optimize_interval=20, iterations=1000, random_seed=2)

# Show Topics
# pprint(lda_mallet.show_topics(num_topics=-1, num_words=20, formatted=False)) # This is the correct one

# Attempting to get a term-topic matrix
tm_results = lda_mallet[corpus]
topics = [[(term, round(wt, 3)) for term, wt in lda_mallet.show_topic(n, topn=20)] for n in range(0, lda_mallet.num_topics)]
topics_df = pd.DataFrame([[term for term, wt in topic] for topic in topics], columns= ['Term'+str(i) for i in range(1,21)], index=['Topic '+str(t) for t in range(1,lda_mallet.num_topics+1)]).T

# print(topics_df.to_string())
topics_df.to_csv('results.csv')



