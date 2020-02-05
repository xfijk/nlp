# getWordStats.py
from auxi import *



if __name__ == '__main__':


	factors = [None]*23

	factors[0] = ['know', 'people', 'think', 'person', 'tell', 'feel', 'friends', 'talk','new', 'talking', 'mean', 'ask', 'understand', 'feelings', 'care','thinking', 'friend', 'relationship', 'realize', 'question', 'answer', 'saying']
	factors[1] = [ 'woke', 'home', 'sleep', 'today', 'eat', 'tired', 'wake', 'watch','watched', 'dinner', 'ate', 'bed', 'day', 'house', 'tv', 'early', 'boring', 'yesterday', 'watching', 'sit' ]
	factors[2] = [ 'years', 'family', 'mother', 'children', 'father', 'kids', 'parents','old', 'year', 'child', 'son', 'married', 'sister', 'dad', 'brother','moved', 'age', 'young', 'months', 'three', 'wife', 'living', 'college','four', 'high', 'five', 'died', 'six', 'baby', 'boy', 'spend','Christmas' ]
	factors[3] = [ 'food', 'eating', 'weight', 'lunch', 'water', 'hair', 'life', 'white','wearing', 'color', 'ice', 'red', 'fat', 'body', 'black', 'clothes','hot', 'drink', 'wear', 'blue', 'minutes', 'shirt', 'green', 'coffee','total', 'store', 'shopping' ]
	factors[4] = [ 'forget', 'forever', 'remember', 'gone', 'true', 'face', 'spent','times', 'love', 'cry', 'hurt', 'wish', 'loved' ]
	factors[5] = [ 'absolutely', 'abundance', 'ace', 'active', 'admirable', 'adore','agree', 'amazing', 'appealing', 'attraction', 'bargain', 'beaming', 'beautiful', 'best', 'better', 'boost', 'breakthrough', 'breeze','brilliant', 'brimming', 'charming', 'clean', 'clear', 'colorful','compliment', 'confidence', 'cool', 'courteous', 'cuddly', 'dazzling','delicious', 'delightful', 'dynamic', 'easy', 'ecstatic','efficient', 'enhance', 'enjoy', 'enormous', 'excellent', 'exotic','expert', 'exquisite', 'flair', 'free', 'generous', 'genius', 'great','graceful', 'heavenly', 'ideal', 'immaculate', 'impressive', 'incredible', 'inspire', 'luxurious', 'outstanding', 'royal', 'speed','splendid', 'spectacular', 'superb', 'sweet', 'sure', 'supreme','terrific', 'treat', 'treasure', 'ultra', 'unbeatable', 'ultimate','unique', 'wow', 'zest' ]
	factors[6] = [ 'wrong', 'stupid', 'bad', 'evil', 'dumb', 'foolish', 'grotesque','harm', 'fear', 'horrible', 'idiot', 'lame', 'mean', 'poor', 'heinous','hideous', 'deficient', 'petty', 'awful', 'hopeless', 'fool', 'risk','immoral', 'risky', 'spoil', 'spoiled', 'malign', 'vicious', 'wicked','fright', 'ugly', 'atrocious', 'moron', 'hate', 'spiteful', 'meager','malicious', 'lacking' ]
	factors[7] = [ 'aggressive', 'alienated', 'angry', 'annoyed', 'anxious', 'careful','cautious', 'confused', 'curious', 'depressed', 'determined','disappointed', 'discouraged', 'disgusted', 'ecstatic', 'embarrassed', 'enthusiastic', 'envious', 'excited', 'exhausted','frightened', 'frustrated', 'guilty', 'happy', 'helpless', 'hopeful','hostile', 'humiliated', 'hurt', 'hysterical', 'innocent', 'interested', 'jealous', 'lonely', 'mischievous', 'miserable', 'optimistic','paranoid', 'peaceful', 'proud', 'puzzled', 'regretful', 'relieved','sad', 'satisfied', 'shocked', 'shy', 'sorry', 'surprised', 'suspicious', 'thoughtful', 'undecided', 'withdrawn' ]
	factors[8] = ['able ', 'able.']
	factors[9] = ['al ', 'al.']
	factors[10] = ['ful ', 'ful.']
	factors[11] = ['ible ', 'ible.']
	factors[12] = ['ic ', 'ic.']
	factors[13] = ['ive ', 'ive.']
	factors[14] = ['less ', 'less.']
	factors[15] = ['ly ', 'ly.']
	factors[16] = ['ous ', 'ous.']
	factors[17] = ['my bad', 'sorry', 'excuse me', 'Excuse me', 'Pardon', 'apologies', 'apology']

	factors[18] = ['shit', 'fuck', 'fucking', 'ass', 'bitch', 'damn', 'hell', 'sucks', 'stupid', 'hate', 'drunk', 'crap', 'kill', 'guy', 'gay', 'kid', 'sex', 'crazy']
	factors[19] = ['bush', 'president', 'Iraq', 'kerry', 'war', 'american', 'political', 'states', 'america', 'country', 'government', 'john', 'national', 'news', 'state', 'support', 'issues', 'article', 'michael', 'bill', 'report', 'public', 'issue', 'history', 'party', 'york', 'law', 'major', 'act', 'fight', 'poor']
	factors[20] = ['game', 'games', 'team', 'win', 'play', 'played', 'playing', 'won', 'season', 'beat', 'final', 'two', 'hit', 'first', 'video', 'second', 'run', 'star', 'third', 'shot', 'table', 'round', 'ten', 'chance', 'club', 'big', 'straight']
	factors[21] = [	'fun', 'im', 'cool', 'mom', 'summer', 'awesome', 'lol', 'stuff', 'pretty', 'ill', 'mad', 'funny', 'weird']
	factors[22] = [	'eyes', 'heart', 'soul', 'pain', 'light', 'deep', 'smile', 'dreams', 'dark', 'hold', 'hands', 'head', 'hand', 'alone', 'sun', 'dream', 'mind', 'cold', 'fall', 'air', 'voice', 'touch', 'blood', 'feet', 'words', 'hear', 'rain', 'mouth']


	# m_name = 'm.test'
	# f_name = 'f.test'

	m_name = 'male'
	f_name = 'female'

	# FC=====================================================
	m_blogs = readGzipBlogs(m_name)
	f_blogs = readGzipBlogs(f_name)

	m_fc_stats = getFcStats(m_blogs, factors)
	f_fc_stats = getFcStats(f_blogs, factors)

	writeFC(m_name, m_fc_stats)
	writeFC(f_name, f_fc_stats)




	# FM=====================================================
	m_tag = readGzipTags(m_name)
	f_tag = readGzipTags(f_name)

	m_fm_stats = getFmStats(m_tag)
	f_fm_stats = getFmStats(f_tag)
	

	writeFM(m_name, m_fm_stats)
	writeFM(f_name, f_fm_stats)
	# stats3 = readFM(f_name)



