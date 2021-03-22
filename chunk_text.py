import shutil
import os

#original_directory = 'book-nlp-master/data/input-txts'
original_directory = '500words/sample!'
#new_directory = '500words'

chunkCounter= 0

for curFile in os.listdir(original_directory):
    print(curFile)
    file = open(original_directory + os.sep + curFile, "rt")
    data = file.read()
    words = data.split()

    counter = 0
    total = 0

    fileText = ""

    for i in range(len(words)):
        counter += 1
        if counter <= 500:
            fileText += " " + words[i]
        else:
            counter = 0
            chunkCounter += 1
            outF = open("fanfic500" + str(chunkCounter) + ".txt", "w")
            outF.write(fileText)
            fileText = ""
            outF.close()

