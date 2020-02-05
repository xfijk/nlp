# auxi.py
import sys
if sys.version_info >= (3, 0):
	from tqdm.autonotebook import tqdm
	import xlrd
	import pprint

	pp = pprint.PrettyPrinter(width=45, compact=True)


import gzip
import io
import os

import nltk.data
nltk.data.path.append("/home/zha34/sfuhome/nltk_data/")
from nltk import word_tokenize
from nltk import pos_tag


from collections import defaultdict


def writeGzipBlogs(f_name, blogs):
	with gzip.open('data/' + f_name + '.blog.gz', 'w' )as output:
		with io.TextIOWrapper(output, encoding='utf-8') as enc:
			for i in range(len(blogs)):
				# print(' '.join([ x[1] for x in pos_tag( word_tokenize(blogs[i])) ] ))
				enc.write( blogs[i]) 
				enc.write( "\n")


def readGzipBlogs(f_name):
	blogs = []
	with gzip.open('data/' + f_name + '.blog.gz', 'r') as f:
		with io.TextIOWrapper(f, encoding='utf-8') as enc:
			# for fl in enc:
			# blogs.append(enc.readline().strip())
			for fl in enc:
				blogs.append(fl.strip())
				# print(fl.strip().split(' '))
	return blogs

def readGzipG(f_name):
	blogs = []
	with gzip.open('data/' + f_name + '.blog.gz', 'r') as f:
		with io.TextIOWrapper(f, encoding='utf-8') as enc:
			for fl in enc:
				blogs.append(fl.strip())
				# print(fl.strip().split(' '))
	return blogs



def writeGzipTagsFromBlogs(f_name, blogs):
	with gzip.open('data/' + f_name + '.tag.gz', 'w' )as output:
		with io.TextIOWrapper(output, encoding='utf-8') as enc:
			for i in tqdm(range(len(blogs))):
				# print(' '.join([ x[1] for x in pos_tag( word_tokenize(blogs[i])) ] ))
				enc.write(' '.join([ x[1] for x in pos_tag( word_tokenize(blogs[i])) ] ))
				enc.write("\n")


def writeGzipTags(f_name, tag_seq):
	with gzip.open('data/' + f_name + '.tag.gz', 'w' )as output:
		with io.TextIOWrapper(output, encoding='utf-8') as enc:
			for i in tqdm(range(len(tag_seq))):
				# print(' '.join([ x[1] for x in pos_tag( word_tokenize(blogs[i])) ] ))
				enc.write(' '.join(tag_seq[i]))
				enc.write("\n")

def readGzipTags(f_name):
	tags = []
	with gzip.open('data/' + f_name + '.tag.gz', 'r') as f:
		with io.TextIOWrapper(f, encoding='utf-8') as enc:
			for fl in enc:
				tags.append(fl.strip().split(' '))
				# print(fl.strip().split(' '))
	return tags


def readGzipTagsStr(f_name):
	tags = []
	with gzip.open('data/' + f_name + '.tag.gz', 'r') as f:
		with io.TextIOWrapper(f, encoding='utf-8') as enc:
			for fl in enc:
				tags.append(fl.strip())
				# print(fl.strip().split(' '))
	return tags


def writeGzipDict(f_name, C_dict, max_len, total):
	with gzip.open('data/' + f_name + '.dict.gz', 'w' )as output:
		with io.TextIOWrapper(output, encoding='utf-8') as enc:

			enc.write( str(total) + '\n' )
			for i in range(max_len):
				enc.write("===\n")
				for k in C_dict[i]:
					enc.write( ' '.join(list(k)) + '==' +  str(C_dict[i][k]) )
					enc.write("\n")


def readGzipDict(f_name, max_len):
	C_dict = []
	count = -1
	with gzip.open('data/' + f_name + '.dict.gz', 'r' )as output:
		with io.TextIOWrapper(output, encoding='utf-8') as enc:

			total = int( enc.readline().strip() )
			for fl in enc:

				fl = fl.strip()

				if fl == '===':
					count += 1
					# sys.stderr.write('\n' + str(count) + '/' + str(max_len) + '\n')
					if count >= max_len:
						break
					C_dict.append(defaultdict(float))

					continue

				kv = fl.split('==')

				k = kv[0].split(' ')
				v = float(kv[1])

				C_dict[count][tuple(k)] = v

	return C_dict, total


def writeTags(f_name, blogs):
	with open('data/' + f_name+ '.tag', 'w' )as f:
		for i in tqdm(range(len(blogs))):
			# print(' '.join([ x[1] for x in pos_tag( word_tokenize(blogs[i])) ] ))
			f.write(' '.join([ x[1] for x in pos_tag( word_tokenize(blogs[i])) ] ))
			f.write("\n")




def readTags(f_name):
	tags = []
	with open('data/' + f_name+ '.tag', 'r') as f:
		for fl in f:
			tags.append(fl.strip().split(' '))
			# print(fl.strip().split(' '))
	return tags



def readData(f_name): # xml <post>
	blogs = []
	with open('data/' + f_name, 'r' ) as f:
		for fl in f:
			blogs.append(fl)
			# break
	return blogs

def readBlogs(f_name): # xml <post>
	blogs = ''
	with open('blogs_m/' + f_name, 'r' ) as f:
		blogs = f.readline().strip()
			# break
	return blogs




def writeData(f_name, blogs): # xml <post>

	with open('data/' + f_name, 'w' ) as f:
		for fl in blogs:
			f.write(fl+'\n')

			# break


def writeData_str(f_name, blogs): # xml <post>

	with open('blogs_m/' + f_name, 'w' ) as f:
		f.write(blogs)

			# break


def readPOS(f_name): # xml <post>
	count = -1
	SP = []
	with open('data/' + f_name + '.POS', 'r' ) as f:
		for fl in f:

			fl = fl.strip()

			if fl == '===':
				count += 1
				SP.append([])
				continue

			if fl:			
				SP[count].append(tuple(fl.split(' ')))
			# break
	return SP


def readPOSAll(f_name): # xml <post>
	count = -1
	SP = []
	with open('data/' + f_name + '.POS', 'r' ) as f:
		for fl in f:

			fl = fl.strip()

			if fl == '===':
				count += 1
				# SP.append([])
				continue

			if fl:			
				SP.append(tuple(fl.split(' ')))
			# break
	return SP


def readPOSAllStr(f_name): # xml <post>
	count = -1
	SP = []
	with gzip.open('stat/' + f_name + '.POS.gz', 'r' ) as f:
		with io.TextIOWrapper(f, encoding='utf-8') as enc:
	# with open('stat/' + f_name + '.POS', 'r' ) as f:
			for fl in enc:

				fl = fl.strip()

				if fl == '===':
					count += 1
					continue

				if fl:			
					SP.append((fl))
	return SP

def writePOS(f_name, SP): # xml <post>

	with open('data/' + f_name + '.POS', 'w' ) as f:
		for sp in SP:
			if len(sp) >=1:
				f.write('===\n')
				for tags in sp:
					f.write(' '.join(list(tags))+'\n' )
			else:
				f.write(' '.join(list(sp))+'\n')

def writePOSAll(f_name, SP): # xml <post>
	with gzip.open('stat/' + f_name + '.POS.gz', 'w' ) as f:
		with io.TextIOWrapper(f, encoding='utf-8') as enc:
	# with open('stat/' + f_name + '.POS', 'w' ) as f:
			for tags in SP:
				# print(list(tags))
				enc.write(' '.join(list(tags))+'\n' )



def countTags(tag_seq, max_len):
	total = [0]*max_len
	C_dict = []
	stat = []

	for i in range(max_len):
		C_dict.append(defaultdict(float))

	for n in tqdm(range(1,max_len+1)):
		for tags in tag_seq:
			for i in range(len(tags)+1-n):
				elem = ()
				for l in range(n):
					elem += (tags[i+l],)

				C_dict[n-1][elem] += 1
				total[n-1] += 1
		

	return C_dict, total


def countTags_2(tag_seq, max_len):
	total = 0
	C_dict = []
	stat = []
	buff = defaultdict(int)

	for i in range(max_len):
		C_dict.append(defaultdict(float))

	for n in tqdm(range(1,max_len+1)):
		for tags in tag_seq:
			for i in range(len(tags)+1-n):
				elem = ()
				for l in range(n):
					elem += (tags[i+l],)
				buff[elem] = 1
			for k in buff:
				C_dict[n-1][k] += 1
			buff.clear()

	return C_dict



def normalizeCount(C_dict, total):
	max_len = len(C_dict)
	# print(total)
	# print(len(total))
	# print(len(C_dict))
	for i in range(max_len):
		for k in C_dict[i]:
			C_dict[i][k] /= float(total)


	# print('sadsa')


def getStats(tags, F):
	stats = []
	for idx in tqdm(range(len(tags))):
		stats.append([])
		for f in F:
			# print(f, end=' ')
			tf = '1' if f in tags[idx] else '0'
			stats[idx].append(tf)
			# print(tf)

	return stats

def getFcStats(tags, factor):
	stats = []
	for idx in tqdm(range(len(tags))):
		stats.append([])
		for fa in factor:
			count = 0
			for w in fa:
				if w in tags[idx]:
					count += 1
			stats[idx].append(count)

	m = 0
	for stat in stats:
		cur = max(stat)
		m = cur if cur > m else m

	# print(m)
	for stat in stats:
		for s in stat:
			s = round( s/float(m)*100)

	stats2 = []

	for stat in stats:
		stats2.append( ' '.join([ str(i) for i in stat])+'\n')

	return stats2

def getFmStats(tag_seq):
	fm = []
	for tags in tag_seq:
		dict_tag = defaultdict(int)
		for t in tags:
			dict_tag[t] += 1

		fm.append(F_meause(dict_tag))
		
	m = 0
	for stat in fm:
		cur = max(stat)
		m = cur if cur > m else m

	stats2 = []
	for stat in fm:
		stats2.append(' '.join([str(round( s/float(m)*1000)) for s in stat])+'\n')

	return stats2

def writeStats(f_name, stats):
	with gzip.open('stat/' + f_name + '.stat.gz', 'w' ) as f:
		with io.TextIOWrapper(f, encoding='utf-8') as enc:
			for s in stats:
				enc.write(' '.join([ str(x) for x in s])+'\n' )


def readStats(f_name):
	stats = []
	# with gzip.open('data/' + f_name + '.tag.gz', 'w' )as output:
	with gzip.open('stat/' + f_name + '.stat.gz', 'r' ) as f:
		with io.TextIOWrapper(f, encoding='utf-8') as enc:
			for fl in enc:
				stats.append([ int(x) for x in fl.strip().split(' ') ])

	return stats

# f measure( for pos)
def writeFM(f_name, fm):
	with gzip.open('stat/' + f_name + '.fm.gz', 'w' ) as f:
		with io.TextIOWrapper(f, encoding='utf-8') as enc:
			for i in fm:
				enc.write(i )


def readFM(f_name):
	fm = []
	with gzip.open('stat/' + f_name + '.fm.gz', 'r' ) as f:
		with io.TextIOWrapper(f, encoding='utf-8') as enc:
			for fl in enc:
				fm.append([ int(x) for x in fl.strip().split(' ') ])

	return fm




# factor class
def writeFC(f_name, fc):
	with gzip.open('stat/' + f_name + '.fc.gz', 'w' ) as f:
		with io.TextIOWrapper(f, encoding='utf-8') as enc:
			for i in fc:
				enc.write(i )


def readFC(f_name):
	fc = []
	with gzip.open('stat/' + f_name + '.fc.gz', 'r' ) as f:
		with io.TextIOWrapper(f, encoding='utf-8') as enc:
			for fl in enc:
				fc.append([ int(x) for x in fl.strip().split(' ') ])

	return fc



def F_meause(C_dict):
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

	noun_freq = noun_count / total_count*1000
	adj_freq = adj_count / total_count*1000
	prep_freq = prep_count / total_count*1000
	art_freq = art_count / total_count*1000
	pron_freq = pron_count / total_count*1000
	verb_freq = verb_count / total_count*1000
	adv_freq = adv_count / total_count*1000
	int_freq = int_count / total_count*1000

	return [noun_freq, adj_freq, prep_freq, art_freq, pron_freq, verb_freq, adv_freq, int_freq ]




	# stats = []
	# for f in F:
	# 	# print(f, end=' ')
	# 	tf = 1 if f in blogs[0] else 0
	# 	stats.append(tf)
	# 	# print(tf)









# Read xlsx, =========================================

def readData_xml(f_name, blogs): # xml
	with open('blogs/' + f_name, 'r' ) as f:
		for fl in f:
			if fl[0] != '<':
				fl = fl.decode('utf-8','ignore').encode('ascii', 'ignore').strip()
				# fl = fl.strip()
				if fl:
					blogs.append(fl)

def readData_xml_doc(f_name): # xml
	blog = ''
	with open('blogs/' + f_name, 'r' ) as f:
		for fl in f:
			if fl[0] != '<':
				fl = fl.decode('utf-8','ignore').encode('ascii', 'ignore').strip()
				# fl = fl.strip()
				if fl:
					blog += ' '+fl
					# blogs.append(fl)
	return blog


def readData_xlsx(f_name):
    workbook = xlrd.open_workbook('data/'+f_name)
    worksheet = workbook.sheet_by_index(0)

    blogs =[]
    gens = []
    g = '1'
    # for row in range(0, 5):
    for row in range(0, worksheet.nrows):
        blogs.append(worksheet.cell_value(row,0).replace('\n', ' ').strip())
        g = '1' if worksheet.cell_value(row,1) == 'M' else '0'
        gens.append(g)

    return blogs, gens

def readData_xlsx_2(f_name):
    workbook = xlrd.open_workbook('data/'+f_name)
    worksheet = workbook.sheet_by_index(0)

    # print(f_name)

    m_blogs =[]
    f_blogs =[]
    # gens = []
    # g = '1'
    # for row in range(0, 10):
    for row in range(0, worksheet.nrows):
        g = '1' if worksheet.cell_value(row,1) == 'M' else '0'
        if g == '1':
        	m_blogs.append(worksheet.cell_value(row,0).replace('\n', ' ').strip())
        else:
        	f_blogs.append(worksheet.cell_value(row,0).replace('\n', ' ').strip())

        # gens.append(g)

    return m_blogs, f_blogs


# # Usage:
# b, g = readData('blog-gender-dataset.xlsx')
# print(b)
# print(g)
# =========================================

