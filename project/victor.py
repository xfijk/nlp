# getFCount.py
from auxi import *
from math import *
from collections import defaultdict
def MI_rank(F):
	prob_class_by_gram=defaultdict(int)
	sum_class_by_gram=defaultdict(int)
	sum_features=0
	prob_class_by_gram, sum_class_by_gram, sum_features=calculate_classes(F)
	print(pro_class_by_gram)
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


def calculate_classes(F):
	F_dict=defaultdict(int);

	#F_dict=F

	max_len = 7

	sys.stderr.write('\n[Couting stats]\n')
	C_dict, total = readGzipDict('f.dev', max_len)


	SP = readPOS('f.dev')



	sum_features=0
	sum_class_by_gram=defaultdict(int)
	prob_class_by_gram=defaultdict(int)
	# example: looking for (RB,) in C_dict.
	#key = ('RB',)
	#print( C_dict[len(key)-1][key])

	for idx,sp in enumerate(SP):
	 	for tags in sp:
	 		F_dict[tags]=C_dict[idx][tags]
	 		print(F_dict[tags])
	 		
	for tags in F_dict:
		sum_features+=F_dict[tags]
	#print(total_c)
	for tags in F_dict:
		sum_class_by_gram[len(tags)]+=F_dict[tags]
	for tags in sum_class_by_gram:
		prob_class_by_gram[tags]+=sum_class_by_gram[tags]/sum_features
	#print (prob_class_by_gram)

	return prob_class_by_gram, sum_class_by_gram , sum_features

def EFS_algorithm(F,Θ,T,w):
	ξ=[]
	ξ[0]=IG_rank(F);
	ξ[1]=MI_rank(F);
	ξ[2]=CHI_rank(F);
	ξ[3]=CE_rank(F);
	ξ[4]=WET_rank(F);
	C_i=[]
	for i in range(1,len(ξ)+1):
		for t_i in range (1,(len(ξ[i-1])/20)+1):
			for t in range(t_i-w,t_i+w):
				if t <=0:
					C_i=C_i
				else:
					temp_C_i=[]
					for j in range(0,t+1):
						temp_C_i.append(ξ[i-1][j])
		C_i.append(temp_C_i)

	OptCandFeatures=[]
	Λ=[]
	for i in range(0,len(C_i[0])):
		for j in range(0,len(C_i)):
			Λ.append(C[j][i])
		OptCandFeatures.append(Λ)
	#20
	Λ_dict=defaultdict(int)
	for Λ_symb in OptCandFeatures:
		Λ_dict[Λ_symb]=??
	return argmax(Λ_dict)








if __name__ == '__main__':
	F_dict=defaultdict(int);
	max_len = 7

	sys.stderr.write('\n[Couting stats]\n')
	C_dict, total = readGzipDict('f.dev', max_len)


	SP = readPOS('f.dev')



	sum_features=0
	sum_class_by_gram=defaultdict(int)
	prob_class_by_gram=defaultdict(int)
	# example: looking for (RB,) in C_dict.
	#key = ('RB',)
	#print( C_dict[len(key)-1][key])

	for idx,sp in enumerate(SP):
	 	for tags in sp:
	 		F_dict[tags]=C_dict[idx][tags]  #F_dict=F
	 		#print(F_dict[tags])
	 		
	for tags in F_dict:
		sum_features+=F_dict[tags]
	#print(total_c)
	for tags in F_dict:
		sum_class_by_gram[len(tags)]+=F_dict[tags]
	for tags in sum_class_by_gram:
		prob_class_by_gram[tags]+=sum_class_by_gram[tags]/sum_features
	#F_dict=sorted(F_dict.items(),key=lambda item:item[1])
	#print(F_dict)
	#print (prob_class_by_gram)
	# print(F_dict)
	# for tags in sum_class_by_gram:
	# 	print (tags)
	#print(sum_class_by_gram[1])
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^6
	#print(pro_class_by_gram)
	MI=defaultdict(int)
	sum_c_others=0
	sum_not_f_in_c=0
	F=F_dict
	for features in F:
		for c_i in prob_class_by_gram: #
			if len(features) == c_i:
				MI[features]+=(F[features]/sum_class_by_gram[len(features)])*prob_class_by_gram[len(features)]*log((F[features]/sum_class_by_gram[len(features)])/(F[features]/sum_features))
		for c_not in prob_class_by_gram: #
			if c_not == len(features):
				MI[features]+=0
			else:
				for c_others in sum_class_by_gram:
					if c_others!=c_not:
						sum_c_others+=sum_class_by_gram[c_others]
					MI[features]+=(F[features]/sum_c_others)*(sum_c_others/sum_features)*log((F[features]/sum_c_others)/(F[features]/sum_features))
		for c_i in prob_class_by_gram: #
			if len(features)==c_i:
				sum_not_f_in_c=sum_class_by_gram[c_i]-F[features]
				MI[features]+=(sum_not_f_in_c/sum_class_by_gram[c_i])*prob_class_by_gram[c_i]*log((sum_not_f_in_c/sum_class_by_gram[c_i])/((sum_features-F[features])/sum_features))
			else:
				MI[features]+=0
		for c_not in prob_class_by_gram:
			sum_c_others+=sum_features-sum_class_by_gram[c_not]
			MI[features]+=((sum_features-F[features])/sum_c_others)*(sum_c_others/sum_features)*log(((sum_features-F[features])/sum_c_others)/((sum_features-F[features])/sum_features))
	MI=sorted(MI.items(), key=lambda item:item[1])
	A=[]
	for i in range(1,3):
		A.append(3)

	print(A)
