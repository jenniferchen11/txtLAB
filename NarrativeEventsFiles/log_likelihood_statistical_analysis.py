#from scipy.stats.distributions import chi2
import scipy.stats as stats
from scipy.stats import chi2_contingency
import math
import csv
import numpy as np

# Conduct log-liklihood test and Fisher’s Exact Test for Odd’s Ratio (assigns p value)
# We want to run these two tests simultaneously in other to determine which of the two datasets is giving the higher likelihood


with open("merged_events.csv", "r") as merged_events:
    i = 0

    ALLRows = csv.reader(merged_events, delimiter=',')
    with open("logLikelihood.csv", "a") as llr_results:
        writer=csv.writer(llr_results)
        for row in ALLRows:
            contingency_table = np.array([[int(row[1]),int(row[2])], [int(row[3]), int(row[4])]])
            oddsratio, pvalue = stats.fisher_exact([[int(row[1]),int(row[2])], [int(row[3]), int(row[4])]])
            i+=1
            #print("Row ", i, ": ", row)
            #print("Log-Liklihood Results: ", chi2_contingency(contingency_table, lambda_="log-likelihood"))
            #print("Odds Ratio: ", oddsratio)
            #print("p-value: ", pvalue)
            #print("\n")
            llr = chi2_contingency(contingency_table, lambda_="log-likelihood")
            llr_gscore = llr[0];

            #Positive = Higher prevalence in NYT
            #Negative = Higher prevalence in fanfics
            if oddsratio < 1:
                llr_gscore = -1*llr_gscore
            #print(llr[0])
            to_append = [row[0], llr_gscore, oddsratio, pvalue]
            writer.writerow(to_append)














# def log_func()
# def tests(row):
#     total = row[1]+row[2]+row[3]+row[4]
#     step1 = sum(total/N*log(k/N+(k==0)))
# H = function(k) {
# 	N = sum(k); 
# 	return(sum(k/N*log(k/N+(k==0))))
# }
# LLR = 2*sum(cont.table)*(H(cont.table)-H(rowSums(cont.table))-H(colSums(cont.table)))

# with open("merged_events.csv", "r") as merged_events:
#     for row in merged_events:
#         total = row[1]+row[2]+row[3]+row[4]
#         log_liklihood_ratio = 2*sum(total)*(log_func(row)=log_func(row[]))
