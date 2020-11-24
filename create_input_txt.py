# Make sure this file is in the main book-nlp-master folder
import os
import argparse

# If --dir is not passed
def write_files():
    for fname in os.listdir(data_path):
        if fname.startswith('.'): # skip hidden files
            continue

        if fname.endswith('.txt'):
            f.write(fname + '\t' + data_path+fname + '\n')

# If --dir is passed
def write_folders():
    for folder in os.listdir(data_path):
        if folder.startswith('.'): # skip hidden files
            continue
            
        for fname in os.listdir(data_path+folder):
            if fname.endswith('.txt'):
                f.write(folder+'__'+fname + '\t' + data_path+folder+'/'+fname + '\n')

                
if __name__ == '__main__':
    data_path = './data/input-txts/'
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', help='If input txts are arranged across different folders', action="store_true")
    args = parser.parse_args()

    f = open('./batch_input.txt', 'w')
    if args.dir:
        print("Assuming that", data_path, "contains folders.")
        write_folders()
    else:
        print("Assuming that", data_path, "contains only txt(s).")
        write_files()
    f.close()