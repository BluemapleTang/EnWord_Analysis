import os,nltk,numpy as np,collections as col,re,pandas as pd
from nltk.stem.wordnet import WordNetLemmatizer
WNL=WordNetLemmatizer()

def from_words(file):
    with open(file,encoding='UTF-8') as txt:
        row_split=re.split(r'[\s]',txt.read().lower())
    row_repeat_words=[]
    for word in row_split:
        if len(word)!=0 and word.isalpha():
            row_repeat_words.append(word)
    return set(row_repeat_words)

senior_words=from_words('Vocabulary_Reference\\senior.txt')
cet4_words=from_words('Vocabulary_Reference\\cet4.txt')
cet6_words=from_words('Vocabulary_Reference\\cet6.txt')
TOEFL_words=from_words('Vocabulary_Reference\\TOEFL.txt')


def get_pos(word):
    ttag=nltk.pos_tag([word])[0][1]
    if ttag.startswith('J'):
        return nltk.corpus.wordnet.ADJ
    elif ttag.startswith('V'):
        return nltk.corpus.wordnet.VERB
    elif ttag.startswith('N'):
        return nltk.corpus.wordnet.NOUN
    elif ttag.startswith('R'):
        return nltk.corpus.wordnet.ADV
    else:
        return ''

def get_txt_words(file):
    with open(file,encoding='UTF-8') as txt:
        row_split=re.split(r'[;,.\s]',txt.read().lower())
    row_repeat_words=[]
    for word in row_split:
        if len(word)!=0 and word.isalpha():
            try:
                row_repeat_words.append(WNL.lemmatize(word,get_pos(word)))
            except:
                row_repeat_words.append(word)         
    row_Counter=col.Counter(row_repeat_words)
    return row_Counter,sorted(row_Counter.items(),\
                        key=lambda x: x[1],reverse=True)

def words_filter(row_list,filter_set):
    return [wordtuple for wordtuple in row_list if wordtuple[0] not in filter_set]

result_list=[]
while(True):    
    filename=input('Document you want open:')
    if filename=='break': 
        break
    counter0,list0=get_txt_words(filename)
    DFrame0=pd.DataFrame(list0,columns=['Word','Frequenty'])
    DFrame0.to_csv(filename[0:-4] + '_word'+'_result.csv')

    senior_up=words_filter(list0,senior_words)
    cet4_up=words_filter(senior_up,cet4_words)
    cet6_up=words_filter(cet4_up,cet6_words)
    TOEFL_up=words_filter(cet6_up,TOEFL_words)

    result_list.append([filename[0:-4],len(list0)-len(senior_up),
    len(senior_up)-len(cet4_up),len(cet4_up)-len(cet6_up),
    len(cet6_up)-len(TOEFL_up),len(list0)-len(TOEFL_up)])

    print('finished!')
    
result_DF=pd.DataFrame(result_list,columns=['FileName','Basic_word','Cet4_word','Cet6_word','TOEFL_word','Advanced_word'])
result_DF.to_csv('FINAL_STATISTICS_RESULT.csv')
print(result_DF)



    
        
    

    







 