import py_entitymatching as em
import numpy
from numpy import block
import pandas as pd


#
# def new_name_feature(ltuple, rtuple):
#     print(rtuple['Name'])
#     # print(em.lev_sim("AB CD","AB C"))
#     return em.lev_sim(ltuple['Name'], rtuple['Name'])



#*************** Load data into dataframe*************************
A=em.read_csv_metadata('Data/books_amazon_clean.csv',key='ID')
B=em.read_csv_metadata('Data/books_millions_clean.csv',key='ID')

# Test dataframe
A_test = A.head(10)
B_test = B.head(10)

# #Blocker 1 AttrEquivalenceBlocker
# b1=em.AttrEquivalenceBlocker()
# C1=b1.block_tables(A, B, "Weight", "Weight", l_output_attrs=['Name'], r_output_attrs=['Name'])
# #print(C1)
#
# #Blocker 2 Overlap
# b2=em.OverlapBlocker()
# C2=b2.block_tables(A,B,'Name','Name',word_level=True,overlap_size=2,l_output_attrs=['Name'], r_output_attrs=['Name'],rem_stop_words= True)
# # print(C2)


# print(A.head)
#Blocker 4 rule based blocker

# r = em.get_feature_fn('jaccard(qgm_2(ltuple[''Name'']),qgm_2(rtuple[''Name'']))',block_t,block_s)




# em.add_feature(block_f,'name_name_lev_sim', r)
b4=em.RuleBasedBlocker()
#****************** Change feature datatype***************************
a_types = em.get_attr_types(A)
b_types = em.get_attr_types(B)
b_types['Name']= a_types['Name']

#******************Create Blocker ***********************************
# block_f = em.get_features_for_blocking(A,B,validate_inferred_attr_types=False)
block_c = em.get_attr_corres(A,B)
block_t = em.get_tokenizers_for_blocking()
block_s = em.get_sim_funs_for_blocking()
block_f=em.get_features(A,B,a_types,b_types,block_c,block_t,block_s)
print (block_f)


#******************************** Add Rules *************************
# b4.add_rule(['Category_Category_jac_dlm_dc0_dlm_dc0(ltuple, rtuple) < 0.5'], block_f)
b4.add_rule(['Author_Author_jac_dlm_dc0_dlm_dc0(ltuple, rtuple) < 0.2'], block_f)
# b4.add_rule([' Publisher_Publisher_jac_dlm_dc0_dlm_dc0(ltuple, rtuple) < 0.3'], block_f)
b4.add_rule([' Name_Name_cos_dlm_dc0_dlm_dc0(ltuple, rtuple) < 0.3'], block_f)
b4.add_rule(['Author_Author_mel(ltuple, rtuple) < 0.5'], block_f)


# New Rule
# b4.add_rule(['name_name_lev_sim(ltuple, rtuple) < 0.8'],block_f)
# b4.add_rule(['Category_Category_lev_sim(ltuple, rtuple) < 0.5'], block_f)

column_names = ['ID','Name', 'Category','Author','Price','Series','Pages','Publisher','Date','Language','ISBN_10','ISBN_13','Dimensions','Weight']
#******************* Blocking step**********************
C = b4.block_tables(A, B, l_output_attrs=column_names, r_output_attrs=column_names)

print(len(C))
C.to_csv('Data/C.csv', index = False)


#**************************** Debug Blocking******************************

D = em.debug_blocker(C, A, B)
print(len(D))
D.to_csv('Data/D.csv', index = False)



#***********************Block further using candidate set C***************************
