import DataCleaner as dc
import TokenInfo as ti
import os
import re


# mode=g.mode
# mode = global_init.mode

def create_mono_gram(READ_DIR):
    one_gram = []
    dc.clean_data()
    os.chdir(READ_DIR)
    index_count=0
    for filename in os.listdir(os.getcwd()):
        file = open(filename, "r")
        contents = file.read()
        tokens = contents.split(" ")
        for token in tokens:
            token=token.strip()
            if(len(token) <= 0):
                continue
            value=token
            is_open=0
            is_close=0
            is_name=0
            index=-1
            if(token[0] == '<'):
                is_open=1
            if(token[-1] == '>'):
                is_close=1
            if(is_open == 1 and is_close ==1):
                is_name=1
            index=index_count
            index_count += 1
            if(is_open==1 or is_close==1):
                value=re.sub(r'\W+','',token)

            tk=ti.token(value, is_open, is_close, is_name, index)
            one_gram.append(tk)
    os.chdir('..')
    return one_gram

def create_bi_gram(READ_DIR,one_gram):
    two_gram = []
    os.chdir(READ_DIR)
    for i in range(0, len(one_gram)-1):
        value=one_gram[i].value+ " "+one_gram[i+1].value
        is_open=0
        if(one_gram[i].is_open == 1 and one_gram[i].is_close == 0):
            is_open=1
        is_close=0
        if(one_gram[i+1].is_close == 1 and one_gram[i+1].is_open == 0):
            is_close=1
        is_name=0
        if(is_open == 1 and is_close == 1):
            is_name=1
        index=one_gram[i].index
        tk=ti.token(value,is_open,is_close,is_name,index)
        two_gram.append(tk)
    os.chdir('..')
    return two_gram

def create_tri_gram(READ_DIR, one_gram):
    three_gram = []
    os.chdir(READ_DIR)
    for i in range(0, len(one_gram)-2):
        value=one_gram[i].value+ " "+one_gram[i+1].value+ " " + one_gram[i+2].value
        is_open=0
        if(one_gram[i].is_open == 1 and one_gram[i].is_close == 0 and one_gram[i+1].is_close == 0):
            is_open=1
        is_close=0
        if(one_gram[i+2].is_close == 1 and one_gram[i+2].is_open == 0 and one_gram[i+1].is_open == 0):
            is_close=1
        is_name=0
        if(is_open == 1 and is_close == 1):
            is_name=1
        index=one_gram[i].index
        tk=ti.token(value,is_open,is_close,is_name,index)
        three_gram.append(tk)
    os.chdir('..')
    return three_gram
