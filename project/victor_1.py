import optparse, sys, os, logging, math
from collections import defaultdict
import nltk
import gzip
import io
from math import pow # in fairSCP
from math import *
# import matplotlib.pyplot as plt
# import numpy as np
def calculate_classes(F):

	F_dict=defaultdict(int);
	num=0
	#print(F)
	for tags in F:
		num=F[tags]
		tags=tags.strip()
		tags=tags.split( ' ')
		#print(tuple(tags))
		#tags=tags.strip()
		F_dict[tuple(tags)]+=num
		# if len(tags)==1:

		# 	F_dict[tuple(tags)]+=num
		# 	#print ((tags[0]))
		# else:
		# 	F_dict[tuple(tags)]+=num
			#print(tuple(tags))
	# for tags in F_dict:
	# 	print(tags,len(tags),F_dict[tags])
	


	#print(F)
	#F_dict=F


	#max_len = 7

	#sys.stderr.write('\n[Couting stats]\n')
	#C_dict, total = readGzipDict('f.dev', max_len)


	#SP = readPOS('f.dev')



	sum_features=0
	sum_class_by_gram=defaultdict(int)
	prob_class_by_gram=defaultdict(int)
	# example: looking for (RB,) in C_dict.
	#key = ('RB',)
	#print( C_dict[len(key)-1][key])

	# for idx,sp in enumerate(F):
	# 	idx=idx+1
	# 	for tags in sp:
	# 		F_dict[tags]=C_dict[idx][tags]
	# 		print(F_dict[tags])
	#print(F_dict)
	for tags in F_dict:
		sum_features+=F_dict[tags]
	#print(total_c)
	for tags in F_dict:
		sum_class_by_gram[len(tags)]+=F_dict[tags]
		#print (tags)
		# if(len(tags)==3):
		# 	print(tags)
	for tags in sum_class_by_gram:
		prob_class_by_gram[tags]+=sum_class_by_gram[tags]/sum_features
	#print (prob_class_by_gram)
	#print("********************************************************")
	#print(prob_class_by_gram, sum_class_by_gram , sum_features)
	#print(sum_features)
	return prob_class_by_gram, sum_class_by_gram , sum_features



def MI_rank(F):
	print("******************")
	prob_class_by_gram=defaultdict(int)
	sum_class_by_gram=defaultdict(int)
	sum_features=0
	prob_class_by_gram, sum_class_by_gram, sum_features=calculate_classes(F)
	print(prob_class_by_gram, sum_class_by_gram, sum_features)
	#print("*************************************")
	#print(pro_class_by_gram)
	MI=defaultdict(int)
	sum_c_others=0
	sum_not_f_in_c=0
	for features in F:
		for c_i in prob_class_by_gram: #11
			if len(features) == c_i:
				MI[features]+=(F[features]/sum_class_by_gram[len(features)])*prob_class_by_gram[len(features)]*log((F[features]/sum_class_by_gram[len(features)])/(F[features]/sum_features))
		for c_not in prob_class_by_gram: #21
			if c_not == len(features):
				MI[features]+=0
			else:
				for c_others in sum_class_by_gram:
					if c_others!=c_not:
						sum_c_others+=sum_class_by_gram[c_others]
				MI[features]+=(F[features]/sum_c_others)*(sum_c_others/sum_features)*log((F[features]/sum_c_others)/(F[features]/sum_features))
		for c_i in prob_class_by_gram: #12
			if len(features)==c_i:
				sum_not_f_in_c=sum_class_by_gram[c_i]-F[features]
				MI[features]+=(sum_not_f_in_c/sum_class_by_gram[c_i])*prob_class_by_gram[c_i]*log((sum_not_f_in_c/sum_class_by_gram[c_i])/((sum_features-F[features])/sum_features))
			else:
				MI[features]+=0
		for c_not in prob_class_by_gram:#22
			sum_c_others+=sum_features-sum_class_by_gram[c_not]
			MI[features]+=((sum_features-F[features])/sum_c_others)*(sum_c_others/sum_features)*log(((sum_features-F[features])/sum_c_others)/((sum_features-F[features])/sum_features))
	MI=sorted(MI.items(), key=lambda item:item[1])
	return MI

def CE_rank(F):
	prob_class_by_gram=defaultdict(int)
	sum_class_by_gram=defaultdict(int)
	sum_features=0
	prob_class_by_gram, sum_class_by_gram, sum_features=calculate_classes(F)
	CE=defaultdict(int)
	P_f=0
	summation=0
	for features in F:
		P_f=F[features]/sum_features
		for c_i in prob_class_by_gram:
			summation+=(sum_class_by_gram[c_i]/F[features])*log((sum_class_by_gram[c_i]/F[features])/(F[features]/sum_features))
		CE[features]+=P_f*summation
	CE=sorted(CE.items(), key=lambda item:item[1])
	return CE


def WET_rank(F):
	WET=defaultdict(int)
	prob_class_by_gram=defaultdict(int)
	sum_class_by_gram=defaultdict(int)
	sum_features=0
	prob_class_by_gram, sum_class_by_gram, sum_features=calculate_classes(F)
	for features in F:
		for c_i in prob_class_by_gram:
			summation+=prob_class_by_gram[tags]*(F[features]/sum_features)*abs(log(sum_class_by_gram[c_i]/F[features]*(1-prob_class_by_gram[c_i])/(prob_class_by_gram[c_i]*(1-sum_class_by_gram[c_i]/F[features]))))
		WET[features]+=summation
	WET=sorted(WET.items(), key=lambda item:item[1])
	return WET
def addsuffix(c,t):
	if c is list:
		c.append(t)
	else:
		temp = []
		temp.append(c)
		temp.append(t)
		c = temp
	return c


def fairSCP(seq, C, k):
	#print("seq:",seq)
	seq_list = seq.split(' ')
	#print("seq_list:",seq_list)

	sum = 0

	for i in range(k):
		seq_1_str = " ".join(str(x) for x in seq_list[i-1])
		seq_2_str = " ".join(str(x) for x in seq_list[i:])
		sum += C[i+1][seq_1_str] * C[k-(i+1)][seq_2_str]

	sum /= (k-1)
	result = pow(C[k][seq], 2)
	return result



def candidate_gen(C, F, k, T):
	C[k] = defaultdict(int)
	for c in F[k-1]:
		#print("F[k-1]:",F[k-1])
		for t in T:
			c_prime = addsuffix(c,t)

			c_prime_seq = " ".join(str(x) for x in c_prime)

			C[k][c_prime_seq] = 0


def readGzipTags(f_name):
	tags = []
	with gzip.open('data/'+f_name + '.gz', 'r') as f:
		with io.TextIOWrapper(f, encoding='utf-8') as enc:
			for fl in enc:
				tags.append(fl.strip().split(' '))
				# print(fl.strip().split(' '))
	return tags



def findSubseq(c,d):
	c_str =" ".join(str(x) for x in c)
	d_str =" ".join(str(x) for x in d)

	return d_str.find(c_str)

def mine_POS_pattern(D, T, minsup, minadherence, MAX_length, n):
	n = 10
	C = {}
	C[0] = defaultdict(int)

	C[1] = defaultdict(int)

	for d in D:
		d_str = d.split(' ')
		#print("d_str:",d_str)
		for t in d_str:
			#print("t:",t)
			C[1][t] += 1

	F = []
	F.append(0) 
	f_count = defaultdict(int)

	temp = []


	for f in C[1]:
		#print("f:",f)
		if C[1][f]/n >= minsup:
			#print("f:",f)
			temp.append(f)

	F.append(temp) 
	#print("F:",F[1])

	SP = []
	SP.append(0) 

	SP.append(F[1])

	k = 2
	for k in range(2,MAX_length+1):

		candidate_gen(C,F,k,T) 
		c_count = defaultdict()

		set_c = []
		for d in D:
			for c in C[k]:
				if c == None:
					break

				if d.find(c) != -1:

					C[k][c] += 1
			
		for c in C[k]:

			if (C[k][c]/n >= minsup):
				set_c.append(c)

		F.append(set_c)

		set_f = []
		C_temp = {}
		C_temp[0] = defaultdict(float)
		
		for i in range(1,k+1):
			C_temp[i] = defaultdict(float)
			for c in C[i]:
				C_temp[i][c] = C[i][c]/n

		#print("F[k]:",F[k])
		for f in F[k]:
			#print("f:",f)
			if fairSCP(f, C_temp, k) >= minadherence:
				set_f.append(f)
		SP.append(set_f)

	return SP, C

def combine_SP_C(SP, C, MAX_length):
	SP_C = defaultdict(int)
	for k in range(1, MAX_length+1):
		for fi in SP[k]:
			SP_C[fi] = C[k][fi] 	
	return SP_C

def IG(C,SP,MAX_length,f):
	# − ∑ P ( c i ) log P ( c i )
	# p(ci) = # occurances of ci / ∑ # occuranves of ci
	f_list = f.split(' ')
	len_f = len(f_list)
	num_c = []
	num_c.append(0)
	total_sum = 0
	for i in range(1, MAX_length+1):
		sum_c = 0
		for fi in SP[i]:
			sum_c += C[i][fi]
		#print("sum_c:",sum_c)
		total_sum += sum_c
		num_c.append(sum_c)
	H = 0
	for i in range(1, MAX_length+1):
		H += (num_c[i]/total_sum)*math.log(num_c[i]/total_sum,2)
	H = -H

	#print("f:",f,"C[len_f][f]:",C[len_f][f])
	p_f = C[len_f][f]/total_sum
	H_relative = 0
	for i in range(1, MAX_length+1):
		p_ci_f = C[len_f][f]/num_c[i]
		p_joint = p_ci_f/p_f
		H_relative += math.log(p_ci_f,2)*p_joint

	return H + H_relative

def rank_IG(C,SP,MAX_length):
	new_SP_dic = defaultdict()
	for gram in range(1,MAX_length+1):
		#print("gram:",gram)
		for fi in SP[gram]:
			#print("fi:",fi)
			new_SP_dic[fi] = IG(C,SP,MAX_length,fi)
	new_SP_list = sorted(new_SP_dic.items(), key=lambda item:item[1])
	return new_SP_list

def cross_entropy(C,SP,MAX_length,f):
	f_list = f.split(' ')
	len_f = len(f_list)
	num_c = []
	num_c.append(0)
	for l in range(1, MAX_length+1):
		num_c.append(0)

	total_sum = 0
	for (fi,score) in SP:
		count_fi = C[len(fi.split(' '))][fi]
		total_sum += count_fi
		num_c[len(fi.split(' '))] += count_fi
	p_f = C[len_f][f]/total_sum

	inner = 0
	for i in range(1, MAX_length+1):
		p_ci_f = C[len_f][f]/num_c[i]
		inner += math.log(p_ci_f/p_f,2)*p_ci_f
	cross_entropy = inner*p_f
	return cross_entropy

def rank_cross_entropy(C,SP,MAX_length):
	new_SP_dic = defaultdict()
	for gram in range(1,MAX_length+1):
		for (fi,score) in SP:
			new_SP_dic[fi] = cross_entropy(C,SP,MAX_length,fi)
	new_SP_list = sorted(new_SP_dic.items(), key=lambda item:item[1])
	return new_SP_list



def find_not_classi(line, SP, i, MAX_length):
	for l in range(1, MAX_length+1):
		if l == i:
			break
		if line.find('new file') != -1:
			return False
		for fi in SP[l]:
			if line.find(fi) != -1:
				return True
	return False

def find_classi(line, SP, i, MAX_length):
	for fi in SP[i]:
		if line.find('new file') != -1:
			return False
		if line.find(fi) != -1:
			return True
	return False

def chi_squre_help(SP,MAX_length,f,i,num_file):
	#print("num_file:",num_file)
	f_list = f.split(' ')
	len_f = len(f_list)
	current_file = []
	file_index = 0
	N = num_file
	W=X=Y=Z=0
	count_f = defaultdict(int)
	count_c = defaultdict(int)
	with open("all_tags","r") as source:
		for line in source:
			#find_nc = find_not_classi(line, SP, i,MAX_length)
			find_ci = find_classi(line, SP, i, MAX_length)
			if line.find('new file') != -1:
				file_index += 1
			else:
				if line.find(f):
					count_f[file_index] += 1
				if find_ci:
					count_c[file_index] += 1

	list_f = []
	list_c = []
	for f in count_f:
		list_f.append(f)
	for c in count_c:
		list_c.append(c)

	for f in list_f:
		for c in list_c:
			if f == c:
				W += 1
			

	for f in list_f:
		for i in range(len(list_c),num_file):
			if f == i:
				X += 1

	for f in range(len(list_f),num_file):
		for c in list_c:
			if f == c:
				Y += 1

	for f in range(len(list_f),num_file):
		for c in range(len(list_c),num_file):
			if f == c:
				Z += 1
	#print("W,X,Y,Z:",W,X,Y,Z)

	num_c = []
	num_c.append(0)
	total_sum = 0
	for i in range(1, MAX_length+1):
		sum_c = 0
		for f in SP[i]:
			sum_c += C[i][f]
		total_sum += sum_c
		num_c.append(sum_c)
	p_ci = num_c[i]/total_sum

	CHI = 0
	CHI = N*(W*Z-Y*X)*(W*Z-Y*X)/(W+Y)*(X+Z)*(W+X)*(Y+Z)
	CHI *= p_ci * CHI
	#print("CHI:",CHI)
	return CHI

def rank_chi_squre(SP,MAX_length,f,num_file):
	sigm_product = 0
	new_SP_dic = defaultdict()
	#new_SP_dic[0] = defaultdict()
	for gram in range(1, MAX_length+1):
		for fi in SP[gram]:
			sigm_product = 0
			for i in range(1, MAX_length+1):
				sigm_product += chi_squre_help(SP,MAX_length,fi,i,num_file)
			new_SP_dic[fi] = sigm_product
	new_SP_list = sorted(new_SP_dic.items(), key=lambda item:item[1])
	return new_SP_list


	
if __name__ == '__main__':
	#tags = readGzipTags('male.tag.small')
	tags = []
	tag_set = defaultdict(int)
	num_file = 10
	with open("all_tags_no_punc_13","r") as source:
		for line in source:
			if line.find('new file') == -1:
				tags.append(line[:len(line)-1])
	num_file += 1
	
	D = tags

	for line in tags:
		line_tag = line.split(' ')
		for t in line_tag:
			tag_set[t] += 0
	T = []
	for t in tag_set:
		T.append(t)



	minsup, minadherence,MAX_length = 10,8,3
	SP, C = mine_POS_pattern(D, T, minsup, minadherence, MAX_length, num_file)

	F=combine_SP_C(SP, C, MAX_length)
	#print(F["PRP"])
	#calculate_classes(F)
	#MI_F=MI_rank(F)
	#print(MI_F)
	CE_F=CE_rank(F)
	print(CE_F)
	# for tags in MI_F:
	# 	print (tags)
	# 	break
	#calculate_classes(F)
	# dictionary=defaultdict(int)
	# dictionary["A"]+=10
	# print()






	# f = SP[2][4]
	# # new_SP_list_CHI = rank_chi_squre(SP,MAX_length,f,num_file)
	# # print(new_SP_list_CHI)
	# new_SP_list_IG = rank_IG(C,SP,MAX_length)

	# new_SP_list_CE = rank_cross_entropy(C,new_SP_list_IG,MAX_length) 
	# print("new_SP_list_IG:",new_SP_list_IG)
	# print("new_SP_list_CE:",new_SP_list_CE)

	

