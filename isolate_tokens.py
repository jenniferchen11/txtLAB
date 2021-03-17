import shutil
import os

original_directory = 'book-nlp-master/batch-output'
new_directory = 'AllTokens'

#shutil.move('book-nlp-master/batch-output/22527.txt/22527.txt.tokens', 'AllTokens/22527.txt.tokens')
#    os.chdir(original_directory+'/'+folder)

for folder in os.listdir(original_directory):
    for curFile in os.listdir(original_directory + '/' + folder):
        print(curFile)
        if curFile.endswith(".tokens"):
            shutil.move(original_directory + '/' + folder + '/' + curFile, new_directory)
