import os
import re

# punctuations=[',','.',';',':','?','!']
def clean_data():
    f = open("mode", "r")
    mode = f.read()
    f.close()

    if(mode =='0'):
        READ_DIR = "train_set"
        WRITE_DIR = "clean_train_set"
    elif(mode =='1'):
        READ_DIR = "test_set"
        WRITE_DIR = "clean_test_set"
    os.chdir(READ_DIR)
    for filename in os.listdir(os.getcwd()):
        file = open(filename, "r")
        contents = file.read()
        contents = re.sub('[^A-Za-z0-9<>/,.?:;!]+',' ',contents)
        clean_contents = ""
        for i in range(0,len(contents)):
            if(i>0 and contents[i]=='>'):
                    if(contents[i - 1] != '/' and contents[i - 1] != '<'):
                        clean_contents+=' '
                    elif(contents[i-1] == '/'):
                        clean_contents+=contents[i]
                        clean_contents+=' '
            elif(i<len(contents)-1 and contents[i]=='<' and contents[i+1]!= '/' and contents[i+1]!='>'):
                clean_contents+=' '
            else:
                clean_contents+=contents[i]
        os.chdir('..')
        os.chdir(WRITE_DIR)
        clean_file = open(filename, "w")
        clean_file.write(clean_contents)
        clean_file.close()
        os.chdir('..')
        os.chdir(READ_DIR)
    os.chdir('..')
#clean_data()