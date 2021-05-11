import os

count = 0

directory = r'500wordchunks'
for filename in os.listdir(directory):
    count += 1
    if count == 3:
        os.remove(directory + os.sep + filename)
        count = 0
