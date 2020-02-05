import os,sys,operator
import nltk
#nltk.download()


path = "blogs/"

def readData_xml(blogs, f_name): # xml
	with open('blogs/' + f_name, 'r' ) as f:
		read = False
		for fl in f:
			if fl[0] != '<':
				fl = fl.decode('utf-8','ignore').encode('ascii', 'ignore').strip()
				# fl = fl.strip()
				if fl:
					blogs.append(fl)

all_blogs = open("all_blogs","w")
file_num = 0
for f in os.listdir(path):
	print("f:",f)
	if f.find('male') == -1: #male boggers
		break
	if file_num == 499:
		break
	with open(os.path.join(path, f), "rb") as source:
		for line in source:
			#print(line)
			if line[0] != '<':
				print("line:",line)
				line = line.decode('utf-8','ignore').encode('ascii', 'ignore').strip()
				print("line:",line)
				if line != '':
					#print("line:",line)
					all_blogs.write(line)
					all_blogs.write("\n")
	all_blogs.write("new file"+"\n")
	file_num += 1
#all_blogs.close()

def is_punc(tag):
	if tag == '(' or tag ==')' or tag == '#' or tag == '``' or tag == "''" or tag == '' or tag == '$' or tag == '.' or tag == ':' or tag == ',':
		print("is tag:",tag)
		return True
	else:
		return False
	return False

all_tags = open("all_tags_no_punc","w")
with open("all_blogs","r") as source:
	for line in source:
		#print("line:",line)
		if line != "new file\n":
			print("write tags")
			words = nltk.word_tokenize(line)
			tags = nltk.pos_tag(words)
			for (word,tag) in tags:
				print("tag:",tag)
				if is_punc(tag) is False:
					all_tags.write(tag+' ')
				else:
					continue
			all_tags.write("\n")
		else:
			all_tags.write("new file"+"\n")
		
all_tags.close()
all_blogs.close()





