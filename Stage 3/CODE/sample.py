import pandas as pd
import py_entitymatching as em


A=em.read_csv_metadata('Data/books_amazon_clean.csv',key='ID')
B=em.read_csv_metadata('Data/books_millions_clean.csv',key='ID')
C=em.read_csv_metadata('Data/C.csv',key='_id', fk_ltable = 'ltable_ID', fk_rtable = 'rtable_ID', ltable = A, rtable = B)


S = em.sample_table(C, 500)
G = S
# Labeled the sample tuple pairs manually
# G = em.label_table(S,'gold_label')
G.to_csv('Data/G.csv', index = False)


