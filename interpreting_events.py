import os
import pandas as pd
from collections import defaultdict

events_file="fanfic_events.csv"
df = pd.read_csv(events_file)
ff_df = pd.DataFrame(df, columns = ['Supersense(verb)', 'Supersense(object)'])
num_rows = ff_df.shape[0]

fanfic_dict_verb = defaultdict(int)
fanfic_dict_obj = defaultdict(int)

for i in range(num_rows):
    fanfic_dict_verb[ff_df['Supersense(verb)'][i]] += 1
    fanfic_dict_obj[ff_df['Supersense(object)'][i]] += 1
    print(i)

with open("interpreting_fanfic_verbs.csv", "w") as f:
    for key in fanfic_dict_verb:
        f.write("%s,%s\n"%(key,fanfic_dict_verb[key]))

with open("interpreting_fanfic_objs.csv", "w") as f:
    for key in fanfic_dict_obj:
        f.write("%s,%s\n"%(key,fanfic_dict_obj[key]))