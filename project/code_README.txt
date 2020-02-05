/data # store blog data 
/stat # store feature data of blogs



auxi.py
	containing auxilary functions
	e.g. read & write file
	     counting statistic

extractblogs.py
	extract all blogs in python2 
	write all blogs with utf-8 encoding so that the blogs can be read in python3

	convert blog sentences into POS tag sequences (using nltk.pos_tag())
	

POS.py
	given tagged sequences, finding the n-gram POS tag features that satisify minsupport and minaddherence 

prepare.py
	counting statistic for input of the 5 criterions
	call EFS.py
	write the ranked feature sequences for the 5 criterions separately 


EFS.py
	ranking feature sequences with the 5 criterations


getFcFmStats.py
	use blog file as input, counting the statistic for different word classes
		(e.g. home, food... ) and f-measure


score_feats.py
	with the ranked feaure list obtained from prepare.py,
	applying them with dynamic thresholds to gen_classify.py



gen_classify.py
	concatenate ranked features (POS) and fc, fm feature
	split the dataset to 9:1 for train:test
	fit train data to a classifier and score it with the test data



# small dataset
http://www.cs.uic.edu/~liub/FBS/blog-gender-dataset.rar

# large dataset
http://u.cs.biu.ac.il/~koppel/BlogCorpus.htm


