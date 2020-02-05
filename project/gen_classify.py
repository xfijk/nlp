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




# def genClassTest(m_name, f_name,  m_stats, f_stats):
def genClassTest(m_name, f_name):
# def genClassTest(m_name, f_name, m_t_name, f_t_name, m_stats, f_stats, m_t_stats, f_t_stats):

    # Training ( 2x9660)
    # m_name = 'male'
    # f_name = 'female'

    # m_name = 'm.test'
    # f_name = 'f.test'
    

    m_stats = readStats(m_name)
    f_stats = readStats(f_name)
    m_fm = readFM(m_name)
    f_fm = readFM(f_name)
    m_fc = readFC(m_name)
    f_fc = readFC(f_name)

    for idx in range(len(m_stats)):
        m_stats[idx] += m_fm[idx]+ m_fc[idx]
        f_stats[idx] += f_fm[idx]+ f_fc[idx]


    m_size = len(m_stats)
    f_size = len(f_stats)#-1
    feat_size = len(m_stats[0])
    total_size = m_size + f_size

    train_cases = np.zeros((total_size, feat_size))
    C = np.zeros(( total_size ))

    for idx in range(m_size):
        train_cases[idx, :] = np.array(m_stats[idx])
        C[idx] = 1
    for idx in range(f_size):
        train_cases[m_size+idx, :] = np.array(f_stats[idx])
        C[m_size+idx] = 0



    # k-fold===============================================
    clf = LogisticRegression( random_state=0, solver='lbfgs', multi_class='multinomial')
    # clf = SVC(C=150,kernel='rbf')
    # clf = LinearSVC(random_state=0, tol=1e-5)
    # clf = MultinomialNB()
    # clf = GaussianNB()
    # clf = BernoulliNB()
    # clf = ComplementNB()
    kf = KFold(n_splits=10, shuffle=True, random_state=4830)
    list_score = []
    for train_idx, test_idx in kf.split(train_cases):
        X_train, y_train = train_cases[train_idx], C[train_idx]
        X_test, y_test = train_cases[test_idx], C[test_idx]
        list_score.append(clf.fit(X_train, y_train).score(X_test, y_test))
        # break

    for i in list_score:
        print(i)
    print('average of 10 rounds : ',sum(list_score)/10)


    # # Testing (3000) ===============================================
    # m_fm = readFM(m_t_name)
    # f_fm = readFM(f_t_name)
    # m_fc = readFC(m_t_name)
    # f_fc = readFC(f_t_name)
    # for idx in range(len(m_t_stats)):
    #     m_t_stats[idx] += m_fm[idx]#+ m_fc[idx]
    #     f_t_stats[idx] += f_fm[idx]#+ f_fc[idx]


    # m_size = len(m_t_stats)
    # f_size = len(f_t_stats)#-1
    # feat_size = len(m_t_stats[0])
    # total_size = m_size + f_size

    # test_cases = np.zeros((total_size, feat_size))
    # t_C = np.zeros(( total_size ))

    # for idx in range(m_size):
    #     test_cases[idx, :] = np.array(m_t_stats[idx])
    #     t_C[idx] = 1
    # for idx in range(f_size):
    #     test_cases[m_size+idx, :] = np.array(f_t_stats[idx])
    #     t_C[m_size+idx] = 0


    # print('the score: ', clf.fit(train_cases, C).score(test_cases, t_C))



if __name__ == '__main__':

    # m_name = 'male'
    # f_name = 'female'

    m_name = 'm.test'
    f_name = 'f.test'
    genClassTest(m_name, f_name)
