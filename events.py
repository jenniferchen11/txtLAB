import os
import pandas as pd
import csv
import sys

#UPDATE
directory = "NYT_tokens/nyt_5"

tri_bi_array = []

for cur_file in os.listdir(directory):
    try:
        path = directory + '/' + cur_file
        df = pd.read_csv(path, sep = "\t", engine = 'python', encoding = 'utf8')
        df_all_necessary_columns = pd.DataFrame(df, columns = ['tokenId', 'headTokenId', 'ner', 'lemma', 'supersense','deprel', 'pos'])
        total_rows = df_all_necessary_columns.shape[0]
        
        #this for loop is locating anchor verbs!!
        for i in range(0, total_rows):#change the end of this range
            hasFoundTrigram = False
            if df_all_necessary_columns['headTokenId'][i] == -1:
                #only look at anchors that are VERBS, fixing issue from round 1
                if df_all_necessary_columns['pos'][i] == 'VB' or df_all_necessary_columns['pos'][i] == 'VBD' or df_all_necessary_columns['pos'][i] == 'VBG' or df_all_necessary_columns['pos'][i] == 'VBN' or df_all_necessary_columns['pos'][i] == 'VBP' or df_all_necessary_columns['pos'][i] == 'VBZ':
                    #print(df_all_necessary_columns['lemma'][i-1], df_all_necessary_columns['lemma'][i], df_all_necessary_columns['tokenId'][i])
                    cur_anchor_verb_token_id = df_all_necessary_columns['tokenId'][i]
                    #locating the subject of all anchor verbs
                    for j in range(i-1, i-11, -1):
                        try:
                            if df_all_necessary_columns['headTokenId'][j] == cur_anchor_verb_token_id and df_all_necessary_columns['deprel'][j] == 'nsubj':
                                #collecting ONLY subjects that are people (ie not it, etc)
                                if df_all_necessary_columns['lemma'][j] == 'I' or df_all_necessary_columns['lemma'][j] == 'she' or df_all_necessary_columns['lemma'][j] == 'he' or df_all_necessary_columns['lemma'][j] == 'we' or df_all_necessary_columns['lemma'][j] == 'they' or df_all_necessary_columns['ner'][j] == 'PERSON' or df_all_necessary_columns['lemma'][j] == 'person' or df_all_necessary_columns['lemma'][j] == 'people':
                                    #print(df_all_necessary_columns['lemma'][j],df_all_necessary_columns['lemma'][i], '|', df_all_necessary_columns['supersense'][i], '| line: ', df_all_necessary_columns['tokenId'][i])
                                    #finding objects (to create trigrams)
                                    for k in range(i+1, i+11):
                                        try:
                                            if df_all_necessary_columns['deprel'][k] == 'dobj' and df_all_necessary_columns['headTokenId'][k] == cur_anchor_verb_token_id:
                                                hasFoundTrigram = True
                                                tri_bi_array.append([df_all_necessary_columns['lemma'][j], df_all_necessary_columns['lemma'][i], df_all_necessary_columns['lemma'][k], df_all_necessary_columns['supersense'][i], df_all_necessary_columns['tokenId'][i]])
                                                #print('object: ', df_all_necessary_columns['lemma'][k], 'line: ', df_all_necessary_columns['tokenId'][i])
                                        except:
                                            continue
                                    if hasFoundTrigram == False:
                                        tri_bi_array.append([df_all_necessary_columns['lemma'][j],df_all_necessary_columns['lemma'][i], '', df_all_necessary_columns['supersense'][i], df_all_necessary_columns['tokenId'][i]])
                                    hasFoundTrigram = False
                        except:
                            continue
        #after every file, update csv
        with open('events.csv', 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(tri_bi_array)
        tri_bi_array = []
        print("-----NEXT FILE-----")
    except:
        print('error outer loop')
        continue  
