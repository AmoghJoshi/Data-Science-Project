import numpy as np
import pandas

# Books Amazon
amazon = pandas.read_csv('Data/books_amazon_output.csv')
print(len(amazon))
unique_amazon = amazon.drop_duplicates(subset='ISBN-10', keep='first', inplace=False)
print(len(unique_amazon))
unique_amazon.to_csv('Data/books_amazon_unique.csv', index = False)

# Books Millions
millions= pandas.read_csv('Data/books_millions_output.csv')
print(len(millions))
unique_millions = millions.drop_duplicates(subset='ISBN-10', keep='first', inplace=False)
print(len(unique_millions))
unique_millions.to_csv('Data/books_millions_unique.csv', index = False)
