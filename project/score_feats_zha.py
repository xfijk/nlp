# score_feats.py

from auxi import *
from svc_try import genClassTest


if __name__ == '__main__':

    m_name = 'male'
    f_name = 'female'
    # m_name = 'old.male'
    # f_name = 'old.female'
    # m_name = 'm.test'
    # f_name = 'f.test'

    rank_ig = readPOSAllStr('ig')
    rank_mi = readPOSAllStr('mi')
    rank_chi = readPOSAllStr('chi')
    rank_ce = readPOSAllStr('ce')
    rank_wet = readPOSAllStr('wet')

    # rank_ig.reverse()
    # rank_mi.reverse()
    # rank_chi.reverse()
    # rank_ce.reverse()
    # rank_wet.reverse()




    w =0# round(len(rank_wet)/100)




    thres = round(len(rank_wet)*0.2) #+ 5
    thres = len(rank_wet)
    # thres = 10
    # thres = 75
    print(len(rank_wet))
    print(thres)
    for idx in tqdm(range(thres-w, thres+w+1)):
        print('the '+ str(idx) + 'th')

        list_feat = sorted(set(rank_ig[:idx] + rank_mi[:idx] + rank_chi[:idx] + rank_ce[:idx] + rank_wet[:idx])) 
        # list_feat = sorted(set( rank_ce[:idx] )) 

        writePOSAll('mix', list_feat)

        # for i in list_feat:
            # print(i)
        
        # print(total)

        list_feat_str = []
        for feat in sorted(list_feat):
            list_feat_str.append(' '.join(list(feat)))
            # print(feat)

        # GetStats=====================================
        m_tags = readGzipTagsStr(m_name)
        f_tags = readGzipTagsStr(f_name)
        # t_tags = readGzipTagsStr('test')

        m_stats = getStats(m_tags, list_feat)
        f_stats = getStats(f_tags, list_feat)
        # t_stats = getStats(t_tags, list_feat_str)

        writeStats(m_name, m_stats)
        writeStats(f_name, f_stats)
        # writeStats('test', t_stats)

        genClassTest(m_name, f_name)
