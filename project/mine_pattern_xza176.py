import optparse, sys, os, logging, math
from collections import defaultdict
import nltk
import gzip
import io
from math import pow # in fairSCP
# import matplotlib.pyplot as plt
# import numpy as np

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
		d_str = d.strip().split(' ')
		#print("d_str:",d_str)
		for t in d_str:
			#print("t:",t)
			C[1][t] += 1

	F = []
	F.append(0) 
	f_count = defaultdict(int)

	temp = []


	for f in C[1]:
		if C[1][f]/n >= minsup:
			temp.append(f)

	F.append(temp) 


	SP = {}
	SP[0] = defaultdict(int)
	SP[1] = defaultdict(int)

	for f in C[1]:
		SP[1][f] = C[1][f]

	k = 2
	for k in range(2,MAX_length+1):
		SP[k] = defaultdict(int)

		candidate_gen(C,F,k,T) 
		c_count = defaultdict(int)

		set_c = []
		for d in D:
			for c in C[k]:
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
		#print("C[k]:",C[k])
		for f in F[k]:
			if fairSCP(f, C_temp, k) >= minadherence:
				#print("f:",f)
				SP[k][f] = C[k][f]

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
	f_list = f.strip().split(' ')
	#print("f:",f)
	#print("f_list:",f_list)
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
	#print("num_c:",num_c)
	for i in range(1, MAX_length+1):
		H += (num_c[i]/total_sum)*math.log(num_c[i]/total_sum,2)
	H = -H

	p_f = C[len_f][f]/total_sum
	p_not_f = 1 - p_f
	
	#f = f
	H_relative = 0
	for i in range(1, MAX_length+1):
		p_ci = num_c[i]/total_sum
		if len_f == i:
			p_f_ci = C[len_f][f]/num_c[i]
		else:
			p_f_ci = 0
		p_ci_f = p_ci*p_f
		#print("p_ci_f:",p_ci_f)
		if p_ci_f != 0:
			H_relative += p_ci_f * math.log(p_ci_f,2)

	#f = not_f
	for i in range(1, MAX_length+1):
		p_ci = num_c[i]/total_sum
		if len_f == i:
			p_not_f_ci = 1 - C[len_f][f]/num_c[i]
		else:
			p_not_f_ci = 0
		p_ci_not_f = p_ci*p_not_f
		if p_ci_not_f != 0:
			H_relative += p_ci_not_f * math.log(p_ci_not_f,2) 

	return H + H_relative

def rank_IG(C,SP,MAX_length):
	new_SP_dic = defaultdict()
	for gram in range(1,MAX_length+1):
		for fi in SP[gram]:
			#print("fi:",fi)
			#print("len(fi):",fi)
			new_SP_dic[fi] = IG(C,SP,MAX_length,fi)
	new_SP_list = sorted(new_SP_dic.items(), key=lambda item:item[1])
	return new_SP_list

def count_gram(C,SP,MAX_length,f):
	f_list = f.strip().split(' ')
	len_f = len(f_list)
	num_c = []
	num_c.append(0)
	for l in range(1, MAX_length+1):
		num_c.append(0)

	total_sum = 0
	for gram in range(1, MAX_length+1):
		for fi in SP[gram]:
			count_fi = C[gram][fi]
			total_sum += count_fi
			num_c[gram] += count_fi
	p_f = C[len_f][f]/total_sum

	return p_f, num_c, total_sum,len_f

def WET(C,SP,MAX_length,f):
	p_f, num_c, total_sum,len_f = count_gram(C,SP,MAX_length,f)

	sigma = 0
	#print("p_f:",p_f)
	for i in range(1,MAX_length+1):
		p_ci = num_c[i]/total_sum
		#print("p_ci:",p_ci)
		if len_f == i:
			p_f_ci = C[len_f][f]/num_c[i]
		else:
			p_f_ci = 0
		p_ci_f = p_ci*p_f
		if p_ci_f*(1-p_ci)/p_ci*(1-p_ci_f) != 0:
			#print("p_ci_f*(1-p_ci)/p_ci*(1-p_ci_f):",p_ci_f*(1-p_ci)/p_ci*(1-p_ci_f))
			sigma += p_ci*p_f*abs(math.log(p_ci_f*(1-p_ci)/p_ci*(1-p_ci_f),2))
	return sigma

def rank_WET(C,SP,MAX_length):
	new_SP_dic = defaultdict()
	for gram in range(1,MAX_length+1):
		for fi in SP[gram]:
			new_SP_dic[fi] = WET(C,SP,MAX_length,fi)
	new_SP_list = sorted(new_SP_dic.items(), key=lambda item:item[1])
	return new_SP_list


def cross_entropy(C,SP,MAX_length,f):
	p_f, num_c, total_sum,len_f = count_gram(C,SP,MAX_length,f)

	inner = 0
	for i in range(1, MAX_length+1):
		p_ci = num_c[i]/total_sum
		if len_f == i:
			p_f_ci = C[len_f][f]/num_c[i]
		else:
			p_f_ci = 0
		p_ci_f =  p_ci*p_f
		if p_ci_f/p_f != 0:
			inner += math.log(p_ci_f/p_f,2)*p_ci_f
	cross_entropy = inner*p_f
	return cross_entropy

def rank_cross_entropy(C,SP,MAX_length):
	new_SP_dic = defaultdict()
	for gram in range(1,MAX_length+1):
		for fi in SP[gram]:
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
	f_list = f.strip().split(' ')
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
	print("W,X,Y,Z:",W,X,Y,Z)

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
	print("p_ci:",p_ci)

	CHI = 0
	CHI = N*(W*Z-Y*X)*(W*Z-Y*X)/(W+Y)*(X+Z)*(W+X)*(Y+Z)
	CHI *= p_ci * CHI
	print("CHI:",CHI)
	return CHI

def rank_chi_squre(SP,MAX_length,num_file):
	sigm_product = 0
	new_SP_dic = defaultdict()
	
	for gram in range(1, MAX_length+1):
		for fi in SP[gram]:
			sigm_product = 0
			for i in range(1, MAX_length+1):
				sigm_product += chi_squre_help(SP,MAX_length,fi,i,num_file)
			new_SP_dic[fi] = sigm_product
	new_SP_list = sorted(new_SP_dic.items(), key=lambda item:item[1])
	return new_SP_list

if __name__ == '__main__':
	tags = []
	tag_set = defaultdict(int)
	num_file = 10
	with open("all_tags_no_punc","r") as source:
		for line in source:
			if line.find('new file') == -1:
				tags.append(line[:len(line)-1])
	print("num_file:",num_file)
	
	D = tags

	for line in tags:
		line_tag = line.strip().split(' ')
		for t in line_tag:
			tag_set[t] += 0
	T = []
	for t in tag_set:
		T.append(t)

	minsup, minadherence,MAX_length = 0.3,0.2,3
	SP, C = mine_POS_pattern(D, T, minsup, minadherence, MAX_length, num_file)

	new_SP_list_IG = rank_IG(C,SP,MAX_length)
	new_SP_list_CE = rank_cross_entropy(C,SP,MAX_length)
	new_SP_list_WET = rank_WET(C,SP,MAX_length)

	print("new_SP_list_IG:",new_SP_list_IG,"\n")
	print("new_SP_list_CE:",new_SP_list_CE,"\n")
	print("new_SP_list_WET:",new_SP_list_WET,"\n")

	list_ig = []
	for (fi, score) in new_SP_list_IG:
		list_ig.append(fi)
	list_ce = []
	for (fi, score) in new_SP_list_CE:
		list_ce.append(fi)
	list_WET = []
	for (fi, score) in new_SP_list_WET:
		list_WET.append(fi)


	if list_ig == list_ce :
		print("ig = ce\n")
	if list_ig == list_WET:
		print("ig = WET")
	if list_ce == list_WET:
		print("ce = WET")

	


