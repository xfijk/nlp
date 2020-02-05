# score_feats.py

from auxi import *
from svc_try import genClassTest



def score_feats():
    m_name = 'male'
    f_name = 'female'
    # m_name = 'old.male'
    # f_name = 'old.female'
    # m_name = 'm.test'
    # f_name = 'f.test'

    # m_t_name = 'm.test'
    # f_t_name = 'f.test'

    rank_ig = readPOSAllStr('ig')
    rank_mi = readPOSAllStr('mi')
    rank_chi = readPOSAllStr('chi')
    rank_ce = readPOSAllStr('ce')
    rank_wet = readPOSAllStr('wet')

    w = round(len(rank_wet)/50)
    w =0
    step = round(2*w/5) 
    step =1# round(2*w/2)


    t_all = round(len(rank_ig)*0.3)
    t_all = 4522
    print(len(rank_ig))
    print(t_all)

    for idx in tqdm(range(-w, w+1, step)):
        print('the '+ str(idx) + 'th')

        # list_feat = sorted(set(rank_ig[:idx+t_ig] + rank_mi[:idx+t_mi] + rank_chi[:idx+t_chi] + rank_ce[:idx+t_ce] + rank_wet[:idx+t_wet])) 
        list_feat = sorted(set(rank_ig[:idx+t_all]  + rank_mi[:idx+t_all] + rank_chi[:idx+t_all] + rank_ce[:idx+t_all] + rank_wet[:idx+t_all])) 
        # list_feat = sorted(set(rank_ig[:idx+t_all] )) 

        # list_feat = sorted(set( rank_ce[:idx] )) 
        
        writePOSAll('mix', list_feat)


        list_feat_str = []
        for feat in sorted(list_feat):
            list_feat_str.append(' '.join(list(feat)))

        # GetStats=====================================
        m_tags = readGzipTagsStr(m_name)
        f_tags = readGzipTagsStr(f_name)
        # m_t_tags = readGzipTagsStr(m_t_name)
        # f_t_tags = readGzipTagsStr(f_t_name)

        m_stats = getStats(m_tags, list_feat)
        f_stats = getStats(f_tags, list_feat)
        # m_t_stats = getStats(m_t_tags, list_feat)
        # f_t_stats = getStats(f_t_tags, list_feat)

        writeStats(m_name, m_stats)
        writeStats(f_name, f_stats)

        genClassTest(m_name, f_name,  m_stats, f_stats)
        # genClassTest(m_name, f_name, m_t_name, f_t_name, m_stats, f_stats, m_t_stats, f_t_stats)



if __name__ == '__main__':
    score_feats()