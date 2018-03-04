from sklearn import svm
from sklearn import tree
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
import numpy as np
import FeatureCreator as fc
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier


f = open("mode","w")
f.write('0')
f.close()
feature_all, n_gram_list =fc.make_features()
labels=fc.get_actual_labels(n_gram_list)
X_TRAIN= (np.asarray(feature_all)).transpose()
Y_TRAIN=(np.asarray(labels)).transpose()

def run_logistic_regression(X,Y):
    kf = KFold(n_splits=5, shuffle=True, random_state=0)
    kf.get_n_splits(X)
    precision=0.0
    recall=0.0
    for train_index, test_index in kf.split(X):
        clf_LR = LogisticRegression()
        X_train, X_test = X[train_index], X[test_index]
        Y_train, Y_test = Y[train_index], Y[test_index]
        clf_LR = clf_LR.fit(X_train, Y_train)
        predictions = (clf_LR.predict(X_test))
        for i in range(0, len(predictions)):
            if (predictions[i] < 0.5):
                predictions[i] = 0
            else:
                predictions[i] = 1
        p = precision_recall_fscore_support(Y_test, predictions)
        precision = p[0][1] + precision
        recall = recall + p[1][1]

    print("\nLogistic regression")
    print "Avg precision: ", precision / 5
    print "Avg recall:", recall / 5

def run_linear_regression(X,Y):
    kf = KFold(n_splits=5, shuffle=True, random_state=0)
    kf.get_n_splits(X)
    precision=0.0
    recall=0.0
    for train_index, test_index in kf.split(X):
        regr = linear_model.LinearRegression()
        X_train, X_test = X[train_index], X[test_index]
        Y_train, Y_test = Y[train_index], Y[test_index]
        regr = regr.fit(X_train, Y_train)
        predictions = (regr.predict(X_test))
        for i in range(0, len(predictions)):
            if(predictions[i] < 0.5):
                predictions[i] = 0
            else:
                predictions[i] = 1
        p = precision_recall_fscore_support(Y_test, predictions)
        precision = p[0][1] + precision
        recall = recall + p[1][1]
    print("\nLinear Regression")
    print "Avg precision: ", precision / 5
    print "Avg recall:", recall / 5

def run_random_forest(X,Y):
    kf = KFold(n_splits=5, shuffle=True, random_state=0)
    kf.get_n_splits(X)
    precision=0.0
    recall=0.0
    for train_index, test_index in kf.split(X):
        clf_RF = RandomForestClassifier(n_jobs=2, random_state=0)
        X_train, X_test = X[train_index], X[test_index]
        Y_train, Y_test = Y[train_index], Y[test_index]
        clf_RF = clf_RF.fit(X_train, Y_train)
        predictions = (clf_RF.predict(X_test))
        p = precision_recall_fscore_support(Y_test, predictions)
        precision = p[0][1] + precision
        recall = recall + p[1][1]
    print("\nRandom Forest")
    print "Avg precision: ", precision / 5
    print "Avg recall:", recall / 5

def run_decision_tree(X,Y):
    kf = KFold(n_splits=5, shuffle=True, random_state=0)
    kf.get_n_splits(X)
    precision=0.0
    recall=0.0
    for train_index, test_index in kf.split(X):
        clf_DT = tree.DecisionTreeClassifier()
        X_train, X_test = X[train_index], X[test_index]
        Y_train, Y_test = Y[train_index], Y[test_index]
        clf_DT = clf_DT.fit(X_train, Y_train)
        predictions = (clf_DT.predict(X_test))
        p = precision_recall_fscore_support(Y_test, predictions)
        precision = p[0][1] + precision
        recall = recall + p[1][1]
    print("\nDecision Tree")
    print "Avg precision: ", precision / 5
    print "Avg recall:", recall / 5

def run_svm(X,Y):
    kf = KFold(n_splits=5,shuffle=True,random_state=0)
    kf.get_n_splits(X)
    precision=0.0
    recall=0.0
    for train_index, test_index in kf.split(X):
        clf_SVM = svm.SVC(C=5, kernel='rbf', gamma=.5)
        X_train, X_test = X[train_index], X[test_index]
        Y_train, Y_test = Y[train_index], Y[test_index]
        clf_SVM = clf_SVM.fit(X_train, Y_train)
        predictions = (clf_SVM.predict(X_test))
        p= precision_recall_fscore_support(Y_test, predictions)
        precision= p[0][1]+precision
        recall=recall+p[1][1]
    print("\nSVM")
    print "Avg precision: ",precision/5
    print "Avg recall:",recall/5



def run_svm_test(X_TRAIN,Y_TRAIN, X_TEST, Y_TEST):
    precision=0.0
    recall=0.0
    clf_SVM = svm.SVC(C=5, kernel='rbf', gamma=.5)
    clf_SVM = clf_SVM.fit(X_TRAIN, Y_TRAIN)
    predictions = (clf_SVM.predict(X_TEST))
    p= precision_recall_fscore_support(Y_TEST, predictions)
    precision= p[0][1]+precision
    recall=recall+p[1][1]
    print("\nSVM on test set")
    print "Avg precision: ",precision
    print "Avg recall:",recall


# k-fold validation
run_svm(X_TRAIN,Y_TRAIN)
run_decision_tree(X_TRAIN,Y_TRAIN)
run_random_forest(X_TRAIN,Y_TRAIN)
run_linear_regression(X_TRAIN,Y_TRAIN)
run_logistic_regression(X_TRAIN,Y_TRAIN)



# Test using SVM on test_set
f = open("mode","w")
f.write('1')
f.close()
test_feature_all, n_gram_list =fc.make_features()
test_labels=fc.get_actual_labels(n_gram_list)
X_TEST= (np.asarray(test_feature_all)).transpose()
Y_TEST=(np.asarray(test_labels)).transpose()
print "SVM on Test Data"
run_svm_test(X_TRAIN,Y_TRAIN,X_TEST, Y_TEST)
