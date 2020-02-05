# prepare.py
from POS_2 import *
from EFS import *
# from getStats import *

def F_meause(C_dict):
	tag_freq  = defaultdict()
	total_count = 0
	for tag in C_dict:
		total_count += C_dict[tag]

	noun_count = 0
	adj_count = 0
	prep_count = 0
	art_count = 0
	pron_count = 0
	verb_count = 0
	adv_count = 0
	int_count = 0

	for tag in C_dict:
		# print("tag:",tag)
		if tag == 'NN' or tag == 'NNP' or tag == 'NNPS':
			noun_count += C_dict[tag]
		if tag == 'JJR' or tag == 'JJS' or tag == 'JJ':
			adj_count += C_dict[tag]
		if tag == 'IN':
			prep_count += C_dict[tag]
		if tag == 'DT':
			art_count += C_dict[tag]
		if tag == 'PRP$' or tag == 'PRP':
			pron_count += C_dict[tag]
		if tag == 'VB' or tag == 'VBP' or tag == 'VBD' or tag == 'VBP' or tag == 'VBZ':
			verb_count += C_dict[tag]
		if tag == 'RB' or tag == 'RB' or tag == 'RBR' or tag == 'RBS':
			adv_count += C_dict[tag]
		if tag == 'UH':
			int_count += C_dict[tag]

	noun_freq = noun_count / total_count
	adj_freq = adj_count / total_count
	prep_freq = prep_count / total_count
	art_freq = art_count / total_count
	pron_freq = pron_count / total_count
	verb_freq = verb_count / total_count
	adv_freq = adv_count / total_count
	int_freq = int_count / total_count

	# print("noun_freq:",noun_freq,"adj_freq:",adj_freq,"prep_freq:",prep_freq,"art_freq:",art_freq,"pron_freq:",pron_freq,"verb_freq:",verb_freq,"adv_freq:",adv_freq,"int_freq:",int_freq)

	F = 0.5 * ((noun_freq + adj_freq + prep_freq + art_freq) - (pron_freq + verb_freq + adv_freq + int_freq) + 100)

	return F


if __name__ == '__main__':

	# POS=====================================
	m_C_dict = []
	f_C_dict = []
	m_name = 'm.dev'
	f_name = 'f.dev'
	# t_name = 'test'
	# minsup, minadherence, max_len = 0.3, 0.2, 7
	# minsup, minadherence, max_len = 0.3, 0.2, 7
	
	# sys.stderr.write('\n[Reading gzip m]\n')
	# tag_seq = readGzipTags(m_name)
	# m_total = len(tag_seq)
	# sys.stderr.write('\n[Couting stats m]\n')
	# m_C_dict = countTags_2(tag_seq, max_len)

	# sys.stderr.write('\n[Writing stats m]\n')
	# writeGzipDict(m_name, m_C_dict, max_len, m_total)

	# sys.stderr.write('\n[Reading stats m]\n')
	# m_C_dict, m_total = readGzipDict(m_name, max_len)


	# # sys.stderr.write('\n[Mine_POS m]\n')
	# # T = [x for x in m_C_dict[0] ] 
	# # SP = mine_POS_pats( m_C_dict, T, minsup, minadherence, max_len, float(m_total))
	# # writePOS(m_name, SP)


	# #==============================================================
	# # sys.stderr.write('\n[Reading gzip f]\n')
	# # tag_seq = readGzipTags(f_name)
	# # f_total = len(tag_seq)
	# # sys.stderr.write('\n[Couting stats f]\n')
	# # f_C_dict = countTags_2(tag_seq, max_len)

	# # sys.stderr.write('\n[Writing stats f]\n')
	# # writeGzipDict(f_name, f_C_dict, max_len, f_total)

	# sys.stderr.write('\n[Reading stats f]\n')
	# f_C_dict, f_total = readGzipDict(f_name, max_len)






	# # sys.stderr.write('\n[Mine_POS f]\n')
	# # T = [x for x in f_C_dict[0] ] 
	# # SP = mine_POS_pats( f_C_dict, T, minsup, minadherence, max_len, float(f_total))
	# # writePOS(f_name, SP)



	# # EFS=====================================
	# # max_len = 7
	# total = f_total + m_total

	# f_c = f_total/total
	# m_c = m_total/total

	# m_SP = readPOSAll(m_name)
	# f_SP = readPOSAll(f_name)
	# F = set(m_SP + f_SP)
	# # F = ( list(set(m_SP) - set(f_SP)) + list( set(f_SP) - set(m_SP)) )

	# # for i in sorted(F):
	# # 	print(i)

	# list_feat = rankFeats(F, f_C_dict, m_C_dict, total, f_total, m_total, f_c, m_c )
	# # print(total)

	# list_feat_str = []
	# for feat in sorted(list_feat):
	# 	list_feat_str.append(' '.join(list(feat)))
	# 	# print(feat)

	# GetStats=====================================
	# m_tags = readGzipTagsStr(m_name)
	m_tag = readGzipTags(m_name)
	# print("m_tag[0]",m_tag[0])
	# f_tags = readGzipTagsStr(f_name)
	f_tag = readGzipTags(f_name)
	# t_tag = readGzipTags(t_name)
	# t_tags = readGzipTagsStr('test')

	m_fm = []
	for file in m_tag:
		count_tag_each_male_file = defaultdict(int)
		for tag in file:
			count_tag_each_male_file[tag] += 1

		# break
		m_fm.append(F_meause(count_tag_each_male_file))

	f_fm = []
	for file in f_tag:
		count_tag_each_female_file = defaultdict(int)
		for tag in file:
			count_tag_each_female_file[tag] += 1
		# break
		f_fm.append(F_meause(count_tag_each_female_file))

	# t_fm = []
	# for file in t_tag:
	# 	count_tag_each_female_file = defaultdict(int)
	# 	for tag in file:
	# 		count_tag_each_female_file[tag] += 1
	# 	# break
	# 	t_fm.append(F_meause(count_tag_each_female_file))



	print("f_fm:")
	for idx in tqdm(range(len(f_fm))):
		f_fm[idx] = (round( (f_fm[idx]-40)*1000) )
		print(f_fm[idx])
	print( sum(f_fm)/float(len(f_fm)))
		
	print("m_fm:")
	for idx in tqdm(range(len(m_fm))):
		m_fm[idx] = (round( (m_fm[idx]-40)*1000) )
		print(m_fm[idx])
	print( sum(m_fm)/float(len(m_fm)))

	# print("t_fm:")
	# for idx in tqdm(range(len(t_fm))):
	# 	t_fm[idx] = (round( (t_fm[idx]-40)*1000) )
	# 	print(t_fm[idx])
	# print( sum(t_fm)/float(len(t_fm)))

	# print(len(t_fm))


	writeFM(m_name, m_fm)
	writeFM(f_name, f_fm)
	# writeFM(t_name, t_fm)


