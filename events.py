import os
import pandas as pd
import csv
import sys

#UPDATE
#cur_file = "toks/2002_Baker,Jo_Offcomer_CT.txt.tokens"
directory = "NYT_tokens/nyt_5"

for cur_file in os.listdir(directory):
    try:
        path = directory + '/' + cur_file
        df = pd.read_csv(path, sep = "\t", engine = 'python', encoding = 'utf8')
        df_all_necessary_columns = pd.DataFrame(df, columns = ['tokenId', 'headTokenId', 'ner', 'lemma', 'supersense','deprel'])
        
        #this for loop is locating anchor verbs!!
        for i in range(0, 1000):#change the end of this range
            if df_all_necessary_columns['headTokenId'][i] == -1:
                #print(df_all_necessary_columns['lemma'][i-1], df_all_necessary_columns['lemma'][i], df_all_necessary_columns['tokenId'][i])
                cur_anchor_verb_token_id = df_all_necessary_columns['tokenId'][i]
                j = i
                istrue = True
                #this inner loop is locating the subject of all anchor verbs
                while istrue == True:
                    try:
                        if df_all_necessary_columns['headTokenId'][j-1] == cur_anchor_verb_token_id and df_all_necessary_columns['deprel'][j-1] == 'nsubj':
                            #print(df_all_necessary_columns['lemma'][j-1],df_all_necessary_columns['lemma'][i], '| line: ', df_all_necessary_columns['tokenId'][i])
                            #collecting ONLY subjects that are people (ie not it, etc)
                            if df_all_necessary_columns['lemma'][j-1] == 'I' or df_all_necessary_columns['lemma'][j-1] == 'she' or df_all_necessary_columns['lemma'][j-1] == 'he' or df_all_necessary_columns['lemma'][j-1] == 'we' or df_all_necessary_columns['lemma'][j-1] == 'they' or df_all_necessary_columns['ner'][j-1] == 'PERSON' or df_all_necessary_columns['lemma'][j-1] == 'person' or df_all_necessary_columns['lemma'][j-1] == 'people':
                                print(df_all_necessary_columns['lemma'][j-1],df_all_necessary_columns['lemma'][i], '|', df_all_necessary_columns['supersense'][i], '| line: ', df_all_necessary_columns['tokenId'][i])
                            istrue = False
                        else:
                            j-=1
                    except:
                        break

    except:
        print('error outer loop')
        continue    