# extract_blogs.py
from auxi import *
import os

def extractBlogs_2(str):
	blogs = []
	stop = False

	count = 1
	for f_name in os.listdir("blogs"):
		if stop:
			if count >= 10: break
		if '.'+ str + '.' in f_name:
			# print(f_name)
			count += 1
			# blogs.append(readData_xml_doc(f_name))
			writeData_str(f_name, readData_xml_doc(f_name))

	print(count)

	# for i in blogs:
	# 	print(i)
	# return blogs


def extractBlogs_3(str):
	blogs = []
	stop = False

	count = 1
	for f_name in os.listdir("blogs_m"):
		if stop:
			if count >= 3: break
		if '.'+ str + '.' in f_name:
			# print(f_name)
			count += 1
			blogs.append(readBlogs(f_name))
			# writeData_str(f_name, readData_xml_doc(f_name))
	print(len(blogs))
	writeGzipBlogs( str , blogs)
	# writeGzipTagsFromBlogs(str, blogs)


#==========================
name = 'old.female'
# name = 'old.female'

# training
# extractBlogs_2(name)
# extractBlogs_3(name)

# blogs = readGzipBlogs(name)
# print(len(blogs))
# writeGzipTagsFromBlogs(name, blogs[:372982])


#==========================
# testing

# # 1 file
# blogs, gens = readData_xlsx('blog-gender-dataset.xlsx')
# writeGzipTagsFromBlogs( 'test', blogs)


# # 2 file
m_blogs, f_blogs = readData_xlsx_2('blog-gender-dataset.xlsx')
# print(f_blogs[553])
writeGzipTagsFromBlogs( 'm.test', m_blogs[:1546])
writeGzipTagsFromBlogs( 'f.test', f_blogs[:1546])
writeGzipBlogs( 'm.test', m_blogs[:1546])
writeGzipBlogs( 'f.test', f_blogs[:1546])



# writeGzipBlogs( 'test.g', gens)

# for i in m_blogs:
# 	print(i)

# blogs = readGzipTags('test')
# gens = readGzipBlogs('test.g')

# for b,g in zip(blogs, gens):
# 	print(b)
# 	print(g)
# 	print()



# print(';goushi')

# t_name = 'test'
# t_blogs = readGzipBlogs(t_name)

# print(len(t_blogs))
# print(t_blogs[0])