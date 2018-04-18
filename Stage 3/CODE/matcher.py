import pandas as pd
import py_entitymatching as em

seed = 0
#**********************Read Labeled Sample Data **********************************
A=em.read_csv_metadata('Data/books_amazon_clean.csv',key='ID')
B=em.read_csv_metadata('Data/books_millions_clean.csv',key='ID')

# A = A.drop(['ISBN_10','ISBN_13'],1)
# B = B.drop(['ISBN_10','ISBN_13'],1)
#
G=em.read_csv_metadata('Data/G.csv',key='_id', fk_ltable = 'ltable_ID', fk_rtable = 'rtable_ID', ltable = A, rtable = B)
# G = G.drop(['ltable_ISBN_10','rtable_ISBN_10'],1)

#**********************Split into Train(I) and Test(J) data***********************
IJ = em.split_train_test(G,train_proportion=0.5, random_state=0)
I = IJ['train']
J = IJ['test']
I.to_csv('Data/I.csv', index = False)
J.to_csv('Data/J.csv', index = False)

#**********************Instantiating the Learning-Based Matchers***********************************************

dt = em.DTMatcher(name='DecisionTree', random_state=0)
svm = em.SVMMatcher(name='SVM', random_state=0)
rf = em.RFMatcher(name='RF', random_state=0)
lg = em.LogRegMatcher(name='LogReg', random_state=0)
ln = em.LinRegMatcher(name='LinReg')
nb = em.NBMatcher(name = 'Naive Bayes')


#**********************Creating Features *******************************************************

#************* Change feature datatype*****************
a_types = em.get_attr_types(A)
b_types = em.get_attr_types(B)
b_types['Name']= a_types['Name']

match_c = em.get_attr_corres(A,B)
match_t = em.get_tokenizers_for_blocking()
match_s = em.get_sim_funs_for_blocking()

F = em.get_features(A,B,a_types,b_types,match_c, match_t, match_s,)

#***********************          Drop Attributes: ISBN_10 and ISBN_13          *****************************************************

drop_list_index = [47,48,49,50,51,52]
F =F.drop(drop_list_index)
print(F.feature_name)


#***********************         Extracting Feature Vectors     *********************************************
# Convert the I into a set of feature vectors using F
H = em.extract_feature_vecs(I,
                            feature_table= F,
                            attrs_after='label',
                            show_progress=False)

# print(H.head())

#*******************Checking / Impute for missing values **********************************************************
# print(any(pd.notnull(H)))

# Impute feature vectors with the mean of the column values.
H = em.impute_table(H, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], strategy='mean')

# print(any(pd.notnull(H)))



#**************************   Select the best ML matcher     *********************************************************

result = em.select_matcher([dt, rf, svm, ln, lg, nb], table=H, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'],
        k=5,target_attr='label', metric_to_select_matcher='f1', random_state=0)

print(result['cv_stats'])




#************************   Display Results *****************************************************
print(result['drill_down_cv_stats']['precision'])
print(result['drill_down_cv_stats']['recall'])
print(result['drill_down_cv_stats']['f1'])




#**************************      Compute Accuracy of Test Set J         ***********************************************************

#************Function to calculate accuracy ********************
def compute_accuracy_J(matcher,return_probs_arg, H, J):
    # Train using feature vectors from I
    matcher.fit(table=H, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], target_attr='label')

    # Convert J into a set of feature vectors using F
    L = em.extract_feature_vecs(J, feature_table=F,
                                attrs_after='label', show_progress=False)
    # Impute L
    L = em.impute_table(L, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], strategy='mean')

    # Predict on L
    predictions = matcher.predict(table=L, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], append=True,
                                  target_attr='predicted', inplace=False, return_probs=return_probs_arg, probs_attr='proba')
    # print(predictions.head())

    # Evaluate the predictions
    eval_result = em.eval_matches(predictions, 'label', 'predicted')
    em.print_eval_summary(eval_result)



#**************** Compute accuracy for each ML model*************************************************

dt = em.DTMatcher(name='DecisionTree', random_state=0)
svm = em.SVMMatcher(name='SVM', random_state=0)
rf = em.RFMatcher(name='RF', random_state=0)
lg = em.LogRegMatcher(name='LogReg', random_state=0)
ln = em.LinRegMatcher(name='LinReg')
nb = em.NBMatcher(name = 'Naive Bayes')

all_matchers = [dt,svm,rf,lg,ln, nb]
return_probs = [True,False,True,True,True, True]
ML_model = ['Decision Tree', 'SVM' ,'Random Forest' ,'Logistic Regression' ,'Linear Regression', 'Naive Bayes']
print("\n\n")
print("Compute accuracy on Test set J and trained on Set I")
print("\n\n")
for i in range(0,len(all_matchers)):
    print("For " + ML_model[i])
    compute_accuracy_J(all_matchers[i],return_probs[i],H,J)
    print("**************************************************************")











