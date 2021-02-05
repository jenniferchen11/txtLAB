import os
import pandas as pd
import sys

#UPDATE
#cur_file = "2002_Baker,Jo_Offcomer_CT.txt.tokens"
directory = "toks"
total_words = 0
character_words = 0

# df = pd.read_csv(cur_file, sep = "\t")
# df1 = pd.DataFrame(df, columns = ['deprel'])
# my_array = df1['deprel'].value_counts().tolist()

print(character_words)
for cur_file in os.listdir(directory):
    df = pd.read_csv(cur_file, sep = "\t")
    df1 = pd.DataFrame(df, columns = ['deprel'])
    my_array = df1['deprel'].value_counts().tolist()
    total_words += df1.shape[0]
    total_words -= my_array[0]

    df2 = pd.DataFrame(df, columns = ['ner', 'lemma'])
    character_search = df2['ner'].value_counts().index.tolist()
    index_PERSON = character_search.index("PERSON")
    character_search2 = df2['ner'].value_counts().tolist()
    num_PERSON = character_search2[index_PERSON]

    #she, he, they
    character_search3 = df2['lemma'].value_counts().index.tolist()
    index_SHE = character_search3.index("she")
    index_HE = character_search3.index("he")
    index_THEY = character_search3.index("they")
    character_search4 = df2['lemma'].value_counts().tolist()
    num_SHE = character_search4[index_SHE]
    num_HE = character_search4[index_HE]
    num_THEY = character_search4[index_THEY]
    character_words = character_words + num_PERSON + num_SHE + num_HE + num_THEY

print("Character Centrism Ratio: ", character_words/total_words)

#print(pd.read_csv(path,use_cols = ['deprel']))
