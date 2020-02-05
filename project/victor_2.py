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

    #max_len = 7

    #sys.stderr.write('\n[Couting stats]\n')
    C_dict, total = readGzipDict('f.dev', max_len)


    #SP = readPOS('f.dev')



    sum_features=0
    sum_class_by_gram=defaultdict(int)
    prob_class_by_gram=defaultdict(int)
    # example: looking for (RB,) in C_dict.
    #key = ('RB',)
    #print( C_dict[len(key)-1][key])

    for idx,sp in enumerate(F):
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
        Λ_dict[Λ_symb]=0
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
    #   print (tags)
    #print(sum_class_by_gram[1])
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #print(pro_class_by_gram)
    # MI=defaultdict(int)
    # sum_c_others=0
    # sum_not_f_in_c=0
    # F=F_dict
    # for features in F:
    #   for c_i in prob_class_by_gram: #
    #       if len(features) == c_i:
    #           MI[features]+=(F[features]/sum_class_by_gram[len(features)])*prob_class_by_gram[len(features)]*log((F[features]/sum_class_by_gram[len(features)])/(F[features]/sum_features))
    #   for c_not in prob_class_by_gram: #
    #       if c_not == len(features):
    #           MI[features]+=0
    #       else:
    #           for c_others in sum_class_by_gram:
    #               if c_others!=c_not:
    #                   sum_c_others+=sum_class_by_gram[c_others]
    #               MI[features]+=(F[features]/sum_c_others)*(sum_c_others/sum_features)*log((F[features]/sum_c_others)/(F[features]/sum_features))
    #   for c_i in prob_class_by_gram: #
    #       if len(features)==c_i:
    #           sum_not_f_in_c=sum_class_by_gram[c_i]-F[features]
    #           MI[features]+=(sum_not_f_in_c/sum_class_by_gram[c_i])*prob_class_by_gram[c_i]*log((sum_not_f_in_c/sum_class_by_gram[c_i])/((sum_features-F[features])/sum_features))
    #       else:
    #           MI[features]+=0
    #   for c_not in prob_class_by_gram:
    #       sum_c_others+=sum_features-sum_class_by_gram[c_not]
    #       MI[features]+=((sum_features-F[features])/sum_c_others)*(sum_c_others/sum_features)*log(((sum_features-F[features])/sum_c_others)/((sum_features-F[features])/sum_features))
    # MI=sorted(MI.items(), key=lambda item:item[1])
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # CE=defaultdict(int)
    # P_f=0
    # summation=0
    # for features in F_dict:
    #   P_f=F_dict[features]/sum_features
    #   for c_i in prob_class_by_gram:
    #       summation+=(sum_class_by_gram[c_i]/F_dict[features])*log((sum_class_by_gram[c_i]/F_dict[features])/(F_dict[features]/sum_features))
    #   CE[features]+=P_f*summation 
    # A=[]
    # for i in range(1,3):
    #   A.append(3)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #print(sum_features,sum_class_by_gram,prob_class_by_gram,F_dict)
    A="CAPABLE"
    words=A
    #words = nltk.word_tokenize(line)
    #tags = nltk.pos_tag(words)
    #print(A.find("AS"))
    GPF=defaultdict(int) #gender preferential features
    GPF["able"]+=0
    GPF["al"]+=0
    GPF["ful"]+=0
    GPF["ible"]+=0
    GPF["ic"]+=0
    GPF["ive"]+=0
    GPF["less"]+=0
    GPF["ly"]+=0
    GPF["ous"]+=0
    GPF["sorry"]+=0
    GPF["apolog"]+=0
    GPF_string=["able","al","ful","ible","ic","ive","less","ly","ous","sorry","apolog"]

    FAWS=defaultdict(int)   #Factor Analysis and Word Classes
    FAWS["Conversation"]+=0
    FAWS["Home"]+=0
    FAWS["Family"]+=0
    FAWS["Food/Clothes"]+=0
    FAWS["Romance"]+=0
    FAWS["Positive"]+=0
    FAWS["Negative"]+=0
    FAWS["Emotion"]+=0

    Conversation = ['know', 'people', 'think', 'person', 'tell', 'feel', 'friends', 'talk', 'new', 'talking', 'mean', 'ask', 'understand', 'feelings', 'care', 'thinking', 'friend', 'relationship', 'realize', 'question', 'answer', 'saying']
    Home = [ 'woke', 'home', 'sleep', 'today', 'eat', 'tired', 'wake', 'watch', 'watched', 'dinner', 'ate', 'bed', 'day', 'house', 'tv', 'early', 'boring', 'yesterday', 'watching', 'sit' ]
    Family = [ 'years', 'family', 'mother', 'children', 'father', 'kids', 'parents', 'old', 'year', 'child', 'son', 'married', 'sister', 'dad', 'brother', 'moved', 'age', 'young', 'months', 'three', 'wife', 'living', 'college', 'four', 'high', 'five', 'died', 'six', 'baby', 'boy', 'spend', 'Christmas' ]
    Food = [ 'food', 'eating', 'weight', 'lunch', 'water', 'hair', 'life', 'white', 'wearing', 'color', 'ice', 'red', 'fat', 'body', 'black', 'clothes', 'hot', 'drink', 'wear', 'blue', 'minutes', 'shirt', 'green', 'coffee', 'total', 'store', 'shopping' ]
    Romance = [ 'forget', 'forever', 'remember', 'gone', 'true', 'face', 'spent', 'times', 'love', 'cry', 'hurt', 'wish', 'loved' ]
    Positive = [ 'absolutely', 'abundance', 'ace', 'active', 'admirable', 'adore', 'agree', 'amazing', 'appealing', 'attraction', 'bargain', 'beaming',  'beautiful', 'best', 'better', 'boost', 'breakthrough', 'breeze', 'brilliant', 'brimming', 'charming', 'clean', 'clear', 'colorful', 'compliment', 'confidence', 'cool', 'courteous', 'cuddly', 'dazzling', 'delicious', 'delightful', 'dynamic', 'easy', 'ecstatic', 'efficient', 'enhance', 'enjoy', 'enormous', 'excellent', 'exotic', 'expert', 'exquisite', 'flair', 'free', 'generous', 'genius', 'great', 'graceful', 'heavenly', 'ideal', 'immaculate', 'impressive', 'incredible',  'inspire', 'luxurious', 'outstanding', 'royal', 'speed', 'splendid', 'spectacular', 'superb', 'sweet', 'sure', 'supreme', 'terrific', 'treat', 'treasure', 'ultra', 'unbeatable', 'ultimate', 'unique', 'wow', 'zest' ]
    Negative = [ 'wrong', 'stupid', 'bad', 'evil', 'dumb', 'foolish', 'grotesque', 'harm', 'fear', 'horrible', 'idiot', 'lame', 'mean', 'poor', 'heinous', 'hideous', 'deficient', 'petty', 'awful', 'hopeless', 'fool', 'risk', 'immoral', 'risky', 'spoil', 'spoiled', 'malign', 'vicious', 'wicked', 'fright', 'ugly', 'atrocious', 'moron', 'hate', 'spiteful', 'meager', 'malicious', 'lacking' ]
    Emotion = [ 'aggressive', 'alienated', 'angry', 'annoyed', 'anxious', 'careful', 'cautious', 'confused', 'curious', 'depressed', 'determined', 'disappointed', 'discouraged', 'disgusted', 'ecstatic', 'embarrassed',  'enthusiastic', 'envious', 'excited', 'exhausted', 'frightened', 'frustrated', 'guilty', 'happy', 'helpless', 'hopeful', 'hostile', 'humiliated', 'hurt', 'hysterical', 'innocent', 'interested',  'jealous', 'lonely', 'mischievous', 'miserable', 'optimistic', 'paranoid', 'peaceful', 'proud', 'puzzled', 'regretful', 'relieved', 'sad', 'satisfied', 'shocked', 'shy', 'sorry', 'surprised', 'suspicious',  'thoughtful', 'undecided', 'withdrawn' ]




    



    #all_tags = open("all_tags_no_punc","w")
    all_blogs = open("all_blogs","r")
    with open("all_blogs","r") as source:

        for line in source:
            #print("****")
            #print("line:",line)
            if line != "new file\n":
                #print("write tags")
                words = nltk.word_tokenize(line)
                for i in range(0,len(words)):
                    if words[i] in Conversation:
                        FAWS["Conversation"]+=1
                    if words[i] in Home:
                        FAWS["Home"]+=1
                    if words[i] in Family:
                        FAWS["Family"]+=1
                    if words[i] in Food:
                        FAWS["Food/Clothes"]+=1
                    if words[i] in Romance:
                        FAWS["Romance"]+=1
                    if words[i] in Positive:
                        FAWS["Positive"]+=1
                    if words[i] in Negative:
                        FAWS["Negative"]+=1
                    if words[i] in Emotion:
                        FAWS["Emotion"]+=1
                    for j in range(0,len(GPF)):
                        if words[i].find(GPF_string[j])!=-1:
                            if (GPF_string[j]=="sorry"):
                                GPF["sorry"]+=1
                            elif (GPF_string[j]=="apolog"):
                                GPF["apolog"]+=1
                            else:
                                if(len(words[i])-len(GPF_string[j])==words[i].find(GPF_string[j])):
                                    GPF[GPF_string[j]]+=1
                tags = nltk.pos_tag(words)
                #for (word,tag) in tags:
                #print("tag:",tag)
                    # if is_punc(tag) is False:
                    #   all_tags.write(tag+' ')
                    # else:
                    #   continue
                    #all_tags.write("\n")
            # else:
            #   all_tags.write("new file"+"\n")
    for tags in FAWS:
        print (tags, FAWS[tags])
    for tags in GPF:
        print(tags,GPF[tags])
        
#all_tags.close()
all_blogs.close()
