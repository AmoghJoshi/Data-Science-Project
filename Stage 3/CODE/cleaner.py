import pandas
import numpy as np
import csv


def clean(inputfile, outputfile):
    ID = 'ID'
    NAME = 'Name'
    CATEGORY = 'Category'
    AUTHOR = 'Author'
    PRICE = 'Price'
    SERIES = 'Series'
    PAGES = 'Pages'
    PUBLISHER = 'Publisher'
    DATE = 'Date'
    LANGUAGE = 'Language'
    ISBN_10 = 'ISBN_10'
    ISBN_13 = 'ISBN_13'
    DIMENSIONS = 'Dimensions'
    WEIGHT = 'Weight'
    COMMA = ','
    NEW_LINE = '\n'



    df = pandas.read_csv(inputfile)
    df = df.fillna('')
    df.insert(0, 'ID', 1)
    X = df.as_matrix()
    for i in range(0,len(X)):
        X[i][0] = i +1
        for j in range(0,len(X[0])):
            if type(X[i][j]) == str and "#" in X[i][j]:
                X[i][j] = X[i][j].replace("#",",")
                X[i][j] = '"' + X[i][j] + '"'
        print(X[i])

    header = ID+COMMA+NAME+COMMA+CATEGORY+COMMA+AUTHOR+COMMA+PRICE+COMMA+SERIES+COMMA+PAGES+COMMA+PUBLISHER+COMMA+DATE+COMMA+LANGUAGE+COMMA+ISBN_10+COMMA+ISBN_13+COMMA+DIMENSIONS+COMMA+WEIGHT+NEW_LINE
    myFile = open(outputfile, 'w')
    myFile.write(header)
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(X)

    myFile.close()


clean('Data/books_amazon_unique.csv','Data/books_amazon_clean.csv')
clean('Data/books_millions_unique.csv','Data/books_millions_clean.csv')