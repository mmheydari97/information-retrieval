import pandas as pd
import re
import time
import itertools
from search.code.dictionaries import normalizing_dictionary, tokenizing_dictionary, verbs, casefolding, abbreviations
from parsivar import FindStems



def news_retrieval(x):
    ## واکشی خبر
    clean = re.compile('<.*?>')
    x = re.sub(clean, '', x) # remove all tags
    x = ' '.join(x.split()) # multiplespaces to one space
    x = x.strip()

    ## deleting &nbsp; and ...
    x = x.replace('&nbsp;', ' ')
    x = x.replace('&laquo;', '«')
    x = x.replace('&quot;', '«')
    x = x.replace('&raquo;', '»')
    x = x.replace('&quot;', '»')


    x = ' ' + x + ' '

    x = x.replace('»', ' » ')
    x = x.replace('«', ' « ')
    x = x.replace('؟', ' ؟ ')
    x = x.replace(':', ' : ')
    x = x.replace('،', ' ، ')
    x = x.replace('.', ' . ')
    x = x.replace(')', ' ) ')
    x = x.replace('(', ' ( ')
    x = x.replace('-', ' - ')
    x = x.replace('»', ' » ')
    x = x.replace('«', ' « ')
    x = x.replace('/', ' / ')
        # x = ' '.join(x.split()) # multiplespaces to one space
    x = ' '.join(x.split()) # multiplespaces to one space

    x = x.strip()

    return x

# if 'می\u200cکردم'=='می‌کردم':
#     print('yes')


def remove_frequents(x): # x is a list of strings (tokens)
    frequent_words = ['.', '«', '»', 'در','از','،','؟','این','همین',':','که','است','در','می\u200cکردم', 'هم', 'او', 'و', 'وی', 'با', 'چه'
    , 'اینکه', 'کنند', 'اگر', 'من', '!', '(', ')', 'س', 'را', 'بر', 'آن', 'نیز', 'ره', 'به', 'است', 'هست', 'یک', 'یا', 'برای'
    , 'دیگر', 'بود', 'کسی', 'هر', '/', '-'] 
    y = [w for w in x if w not in frequent_words] ## deleting frequent words
    return y


def Normalizing(x): # x is a string
    for key, value in normalizing_dictionary.items():
        for k in key:
            x = x.replace(k, value)
    return x


def CaseFolding(x): # x is a string
    for key, value in casefolding.items():
        x = x.replace(key, value)
    for key, value in abbreviations.items():
        x = x.replace(key, value)
    return x

def Tokenization(x): ## x is a string
    x = ' ' + x + ' '  # fix problem for first and last word

    for key, value in tokenizing_dictionary.items():
        for k in key:
            x = x.replace(k, value)

    x = x.replace(' ها ', '‌‌ها ') # آقای هاشمی problem fixed

    for key, value in verbs.items():
        for k in key:
            x = x.replace(k, value)

    x = ' '.join(x.split()) # multiplespaces to one space
    x = x.strip()

    x = x.split(' ')

    for i in range(len(x)):
        x[i] = re.sub(r'\u200c+', '\u200c', x[i])

    for i in range(len(x)):
        if x[i].endswith('\u200c'):
            x[i] = x[i][:-1]
            
    return x


def Stemming(x):

    my_stemmer = FindStems()
    for i in range(len(x)):
        res = my_stemmer.convert_to_stem(x[i])
        if '&' in res:
            pos = res.find('&')
            res = res[0:pos]

        # solving problem with می‌توانسته‌ام
        if res.startswith('می\u200c') and res!='می‌سی‌سی‌پی':
            res = my_stemmer.convert_to_stem(x[i][3:])
            if '&' in res:
                pos = res.find('&')
                res = res[0:pos]
            elif res.endswith(''):
                res = my_stemmer.convert_to_stem(x[i][:-1])
                if '&' in res:
                    pos = res.find('&')
                    res = res[0:pos]
        x[i] = res
    return x







def add_word(doc_id, list_of_words, dic):
    for i in range(len(list_of_words)):
        position = i
        word = list_of_words[i]
        # print(word)
        if word not in dic:  ### if word is not in the dictionary
            dic[word] = [[doc_id, [i]]]

        else:                  ### if word is in the dictionary
            list_1 = dic[word]
            flag = False
            index = -1
            for j in range(len(list_1)):
                if (list_1[j])[0] == doc_id:
                    flag = True
                    index = j
                    break
                
            if flag: ### if word has more than one occurence in the current doc_id
                tmp = list_1[index]
                tmp[1].append(position)
                list_1[index] = tmp
                dic[word] = list_1
             
            else:   ### if word is occuring for the first time in this doc_id
                list_ = dic[word]
                list_.append([doc_id,[position]])
                dic[word] = list_
            
    return dic


def give_dictionary():
    dic = {}
    # dfs = pd.read_excel('./../../News.xlsx')
    # dfs = pd.read_excel('/home/mohammad/Documents/University/S9/IR/Project/main/News.xlsx')
    dfs = pd.read_csv('IR-F19-Project02-14k.csv')[:1000]
    
    contents = dfs['content']
    # doc_number = [i for i in range(1)]
    doc_number = [i for i in range(len(contents))]
    # doc_number = list(set(doc_number) - set([1702, 1346, 1159, 1068, 1018, 907]))

    for doc_id in doc_number:
        x = contents[doc_id]
        x = news_retrieval(x) # واکشی

        x = Normalizing(x)
        x = CaseFolding(x)

        # print(x)
        x = Tokenization(x) # استخراج توکن
        x = remove_frequents(x)
        # print(x)
     
        x = Stemming(x) ## ریشه یابی

        dic = add_word(doc_id, x, dic) # ایجاد شاخص معکوس مکانی
    
    return dic

# start = time.time()
# dic = give_dictionary()
# end = time.time()
# print(end - start)


# import json
# with open('dict1.txt', 'w') as file:
#     file.write(json.dumps(dic, ensure_ascii=False).encode('utf8').decode())


### code for removing duplicates
# seen = set()
# seen_add = seen.add
# y = [x for x in y if not (x in seen or seen_add(x))]



