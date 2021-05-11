import csv
import os
import sys
import pandas
import numpy
from collections import Counter
from sklearn.utils import resample

for i in range(1000):
    with open('../../NYT_topic_probabilities.csv', "r") as f:
        reader = csv.reader(f)
        next(reader)
        boot = resample([row for row in reader], replace=True, n_samples=82981) #replace n_samples accordingly
        #print(boot)
        csvname = "../../nyt_bootstraps/bootstrap" + str(i+321) + ".csv"
        with open(csvname, "w+", newline ='') as file:
            write = csv.writer(file)
            write.writerows(boot)
