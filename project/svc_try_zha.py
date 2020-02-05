from auxi import *


import numpy as np
import operator
from os import listdir

from sklearn.svm import SVC, SVR, LinearSVC, NuSVR

from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold

from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB, ComplementNB

from sklearn.linear_model import LogisticRegression


def genClassTest(m_name, f_name):

    # Training ( 2x9660)
    # m_name = 'male'
    # f_name = 'female'

    # m_name = 'm.test'
    # f_name = 'f.test'
    


    m_stats = readStats(m_name)
    f_stats = readStats(f_name)
    # m_fm = readFM(m_name)
    # f_fm = readFM(f_name)

    # for idx in range(len(m_stats)):
    #     m_stats[idx].append(m_fm[idx])
    #     f_stats[idx].append(f_fm[idx])



    m_size = len(m_stats)
    f_size = len(f_stats)
    
    feat_size = len(m_stats[0])

    # print(m_size)
    # print(f_size)
    total_size = m_size + f_size

    train_cases = np.zeros((total_size, feat_size))
    # kf = KFold(n_splits=2)



    # C = []
    C = np.zeros(( total_size ))

    for idx in range(m_size):
        train_cases[idx, :] = np.array(m_stats[idx])
        # C.append(1)
        C[idx] = 1
    for idx in range(f_size):
        # print(idx)
        train_cases[m_size+idx, :] = np.array(f_stats[idx])
        # C.append(0)
        C[m_size+idx] = 0

    # for i in C:
    #     print(i)


    # k-fold
    clf = LogisticRegression( random_state=0, solver='lbfgs', multi_class='multinomial')
    # clf = SVC(C=150,kernel='rbf')
    # clf = LinearSVC(random_state=0, tol=1e-5)
    # clf = MultinomialNB()
    # clf = GaussianNB()
    # clf = BernoulliNB()
    # clf = ComplementNB()
    kf = KFold(n_splits=10, shuffle=True)
    list_score = []
    for train_idx, test_idx in kf.split(train_cases):
        X_train, y_train = train_cases[train_idx], C[train_idx]
        X_test, y_test = train_cases[test_idx], C[test_idx]
        list_score.append(clf.fit(X_train, y_train).score(X_test, y_test))
        # break

    for i in list_score:
        print(i)
    print('10-fold: ',sum(list_score)/10)


        # err_num = 0.0


    # # Testing ( 3000 )
    # err_num = 0.0
    # t_name = 'test'
    # t_stats = readStats(t_name)

    # # t_fm = readFM(t_name)
    # # for idx in range(len(t_stats)):
    # #     t_stats[idx].append(t_fm[idx])

    # t_size = len(t_stats)
    # feat_size = len(t_stats[0])
    # gens = readGzipG('test.g')
    # print(len(t_stats))
    # print(len(gens))

    # test_cases = np.zeros((t_size, feat_size))
    # C = np.zeros(( t_size ))

    # for idx in range(t_size):
    #     test_cases[idx, :] = np.array(t_stats[idx])
    #     C[idx] = (int(gens[idx]))

    # # k-fold
    # clf = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial')
    # # clf = LinearSVC(random_state=0, tol=1e-5)
    # kf = KFold(n_splits=10, shuffle=True)
    # list_score = []
    # for train_idx, test_idx in kf.split(test_cases):
    #     clf = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial')
    #     X_train, y_train = test_cases[train_idx], C[train_idx]
    #     X_test, y_test = test_cases[test_idx], C[test_idx]
    #     list_score.append(clf.fit(X_train, y_train).score(X_test, y_test))
    #     print()
    # print()

    # for i in list_score:
    #     print(i)
    # print(sum(list_score)/10)







    # # clf = SVC(C=150,kernel='rbf')
    # clf = LinearSVC(random_state=0, tol=1e-5)
    # clf = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial')
    # # clf = MultinomialNB()
    # # clf = GaussianNB()
    # # clf = BernoulliNB()
    # # clf = ComplementNB()

    # print(': ', clf.fit(train_cases, C).score(train_cases, C))

    # # scores = cross_val_score(clf, train_cases, C, cv=10)
    # # print(scores)
    # # print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))



    # # Testing
    # err_num = 0.0

    # t_stats = readStats(t_name)
    # # t_fm = readFM(t_name)

    # # for idx in range(len(t_stats)):
    # #     t_stats[idx].append(t_fm[idx])

    # t_size = len(t_stats)

    # gens = readGzipG('test.g')

    # for idx in tqdm(range(t_size)):
    #     test_case = np.array( [t_stats[idx] ])
    #     c_out = clf.predict(test_case)
    #     if(c_out != int(gens[idx])):
    #         err_num += 1.0

    # print("wrong for: %d   \n rate   %f%%" % (  err_num, 100-err_num/t_size * 100))


if __name__ == '__main__':

    m_name = 'male'
    f_name = 'female'

    # m_name = 'm.test'
    # f_name = 'f.test'
    genClassTest(m_name, f_name)
