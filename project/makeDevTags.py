from auxi import *
from collections import defaultdict
import imp
# nltk.download('averaged_perceptron_tagger')

from math import pow # in fairSCP


m_tag_seq = readGzipTags('male')
f_tag_seq = readGzipTags('female')

# print(len(tag_seq))

writeGzipTags('m.dev', m_tag_seq[:200] )
writeGzipTags('f.dev', f_tag_seq[:200] )




