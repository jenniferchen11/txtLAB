from scipy.stats.distributions import chi2
from scipy.stats import chi2_contingency
import math
import csv
import pandas as pd
import numpy as np

events_file="interpreting_nyt_events_1000.csv" #put NYT interpreted events file here
#events_file="test.csv"
df_nyt = pd.read_csv(events_file)
num_rows_nyt = df_nyt.shape[0]

events_file="interpreting_fanfic_events_1000.csv" #put fanfic interpreted events file here
#events_file="test2.csv"
df_fanfic = pd.read_csv(events_file)
num_rows_ff = df_fanfic.shape[0]

with open("merged_events.csv", "a") as merged_events:
    writer=csv.writer(merged_events)
    for i in range(num_rows_nyt):
        is_found = False
        for j in range(num_rows_ff):
            if df_nyt.iloc[i, 0] == df_fanfic.iloc[j,0]: #brigram/trigram appears in both
                to_append= [df_nyt.iloc[i,0], df_nyt.iloc[i,1], 1546177-df_nyt.iloc[i,1], df_fanfic.iloc[j,1], 1734263-df_fanfic.iloc[j,1]]
                writer.writerow(to_append)
                is_found = True
        if is_found == False: #if bigram/trigram is in NYT but doesn't appear at all in fan-fic
            writer.writerow([df_nyt.iloc[i,0], df_nyt.iloc[i,1], 1546177-df_nyt.iloc[i,1], 0, 1734263])
    

with open("only_in_fanfics.csv", "w") as only_in_fanfics:
    writer=csv.writer(only_in_fanfics)
    with open("merged_events.csv", "r") as merged_events:
        csv_reader = csv.reader(merged_events)
        for i in range(num_rows_ff):
            bi_tri_found = False
            for row in csv_reader:
                # print(df_fanfic.iloc[i, 0])
                # print(row[0])
                # print('\n')
                if df_fanfic.iloc[i,0] == row[0]: #issue is probably here
                    print("FOUND")
                    bi_tri_found = True
                    print(bi_tri_found)
                    break
            if bi_tri_found == False:
                writer.writerow([df_fanfic.iloc[i, 0], 0, 1546177, df_fanfic.iloc[i, 1], 1734263-df_fanfic.iloc[i, 1]])

with open("merged_events.csv", "a") as merged_events:
    writer=csv.writer(merged_events)
    with open("only_in_fanfics.csv", "r") as only_in_fanfics:
        csv_reader = csv.reader(only_in_fanfics)
        for row in csv_reader:
            writer.writerow(row)


