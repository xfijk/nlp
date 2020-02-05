# EFS.py
from auxi import *


from math import log, pow



def ig_score(feat, _feat, m_c, f_c, m_cf, f_cf, m_c_f, f_c_f):
	en_c = - m_c * log(m_c) - f_c * log(f_c)
	# print(_feat , m_c_f  , f_c_f  )
	en_cf = feat * ( m_cf * log(m_cf) + f_cf * log(f_cf) ) + \
			_feat * ( m_c_f * log(m_c_f) + f_c_f * log(f_c_f) )


	res = en_c + en_cf
	# print(res)
	return res

def mi_score(feat, _feat, m_c, f_c, m_cf, f_cf, m_c_f, f_c_f):
	fc_m = feat* m_cf* log(m_cf/ m_c)
	_fc_m = _feat* m_c_f* log(m_c_f/ m_c)
	# f_c_m = feat* f_cf* log(f_cf/ f_c)
	# _f_c_m = _feat* f_c_f* log(f_c_f/ f_c)

	fc_f = feat* f_cf* log(f_cf/ f_c)
	_fc_f = _feat* f_c_f* log(f_c_f/ f_c)
	# f_c_f = feat* m_cf* log(m_cf/ m_c)
	# _f_c_f = _feat* m_c_f* log(m_c_f/ m_c)

	res = (fc_m + _fc_m + fc_f + _fc_f )
	return res

def chi_score(total, m_total, f_total, feat_num, m_feat_num, f_feat_num ):
	w_y = m_total
	x_z = f_total
	w_x = feat_num
	y_z = total - feat_num

	n = total 

	wz = m_feat_num* ( f_total - f_feat_num)
	yx = f_feat_num* ( m_total - m_feat_num)

	top = total* pow((wz - yx), 2)
	bot = w_y* x_z* w_x* y_z

	res = top/bot
	return res

def ce_score(feat, m_cf, f_cf):
	fc_m = feat* m_cf* log(m_cf/ feat)
	fc_f = feat* f_cf* log(f_cf/ feat)

	res = (fc_m + fc_f )
	return res

def wet_score(feat, m_c, f_c, m_cf, f_cf):
	m_res = m_c* feat* abs( log( (m_cf* f_c)/ (m_c* f_cf) ) ) 
	f_res = f_c* feat* abs( log( (f_cf* m_c)/ (f_c* m_cf) ) ) 

	res = (m_res + f_res )
	return res




def rankFeats(F, f_C_dict, m_C_dict, total, f_total, m_total, f_c, m_c ):
	list_ig = []
	list_mi = []
	list_chi = []
	list_ce = []
	list_wet = []
	sys.stderr.write('\n[IG]\n')
	for f in F:
		# print(len(f))
		size = len(f)-1
		
		m_feat_num = m_C_dict[size][f]
		f_feat_num = f_C_dict[size][f]
		feat_num = f_feat_num + m_feat_num
		# print(m_feat_num)
		feat = feat_num / total
		if feat == 1 or m_feat_num == 0 or f_feat_num == 0 :
			continue
		_feat = 1 - feat


		m_cf = m_feat_num / feat_num 
		m_c_f = (m_total - m_feat_num) / (total - feat_num) 

		f_cf = f_feat_num / feat_num 
		f_c_f = (f_total - f_feat_num) / (total - feat_num)

		if m_c_f == 0 or f_c_f == 0 : 
			continue

		
		score_ig = ig_score(feat, _feat, m_c, f_c, m_cf, f_cf, m_c_f, f_c_f)
		score_mi = mi_score(feat, _feat, m_c, f_c, m_cf, f_cf, m_c_f, f_c_f)
		score_chi = chi_score(total, m_total, f_total, feat_num, m_feat_num, f_feat_num)
		score_ce = ce_score(feat, m_cf, f_cf)
		score_wet = wet_score(feat, m_c, f_c, m_cf, f_cf) 
		list_ig.append((score_ig, f))
		list_mi.append((score_mi, f))
		list_chi.append((score_chi, f))
		list_ce.append((score_ce, f))
		list_wet.append((score_wet, f))


	rank_ig = [ k[1] for k in sorted(list_ig, key=lambda x: x[0], reverse=True) ]
	rank_mi = [ k[1] for k in sorted(list_mi, key=lambda x: x[0], reverse=True) ]
	rank_chi = [ k[1] for k in sorted(list_chi, key=lambda x: x[0], reverse=True) ]
	rank_ce = [ k[1] for k in sorted(list_ce, key=lambda x: x[0], reverse=False) ]
	rank_wet = [ k[1] for k in sorted(list_wet, key=lambda x: x[0], reverse=True) ]


	writePOSAll('ig', rank_ig)
	writePOSAll('mi', rank_mi)
	writePOSAll('chi', rank_chi)
	writePOSAll('ce', rank_ce)
	writePOSAll('wet', rank_wet)




	# return list_rank



if __name__ == '__main__':
	m_name = 'm.dev'
	f_name = 'f.dev'


	max_len = 7
	sys.stderr.write('\n[Couting stats]\n')
	m_C_dict, m_total = readGzipDict(m_name, max_len)
	f_C_dict, f_total = readGzipDict(f_name, max_len)

	total = f_total + m_total

	f_c = f_total/total
	m_c = m_total/total


	m_SP = readPOSAll(m_name)
	f_SP = readPOSAll(f_name)

	# F = ( list(set(m_SP) - set(f_SP)) + list( set(f_SP) - set(m_SP)) )
	F = set(m_SP + f_SP)

	# for m, f in zip(m_SP, f_SP):
	# 	F += set(m + f)

	# for i in sorted(F):
	# 	print(i)

	# print(total)

	list_ig = rankFeats(F, f_C_dict, m_C_dict, total, f_total, m_total, f_c, m_c )
	# for feat in sorted(list_ig):
	# 	print(feat)
	writePOSAll('mix', list_ig)
	# writePOSAll('ig', list_ig)
	# writePOSAll('mi', list_ig)
	# writePOSAll('chi', list_ig)
	# writePOSAll('ce', list_ig)
	# writePOSAll('wet', list_ig)