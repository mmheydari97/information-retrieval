import pandas as pd
import re
from hazm import *
import time
import itertools
# # from bs4 import BeautifulSoup as BS



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
    x = ' '.join(x.split()) # multiplespaces to one space

    return x

# if 'می\u200cکردم'=='می‌کردم':
#     print('yes')

def Normalizing(x):
    normalizer = Normalizer()
    x = normalizer.normalize(x)
    return x

def CaseFolding(x):
    x = x.replace('اطاق','اتاق')
    x = x.replace('آیینه','آینه')
    x = x.replace('هیات','هیئت')
    x = x.replace('طوسی','توسی')
    x = x.replace('بلیط','بلیت')
    x = x.replace('ذغال','زغال')
    x = x.replace('اسطبل','اصطبل')
    x = x.replace('آ', 'ا')
    
    return x

def Tokenization(x): ## Tokenization
    x = word_tokenize(x)
    return x


def Stemming(x):

    for i in range(len(x)):
        x[i] = x[i].replace('پرندگان', 'پرنده')
        x[i] = x[i].replace('حشرات', 'حشره')
        x[i] = x[i].replace('مسابقات', 'مسابقه')

        # تشنگان گرسنگان ستارگان نویسندگان شنوندگان چوگان زندگان آسودگان سیستان بلوچستان
        # خاطرات سبزیجات زبان دهان

        x[i] = re.sub(r'\u200cهایی$', '', x[i])
        x[i] = re.sub(r'هایی$', '', x[i])
        x[i] = re.sub(r'\u200cهای$', '', x[i])
        x[i] = re.sub(r'های$', '', x[i])
        x[i] = re.sub(r'\u200cها$', '', x[i])
        x[i] = re.sub(r'ها$', '', x[i])

        x[i] = re.sub(r'ان$', '', x[i])

        x[i] = re.sub(r'ات$', '', x[i])


        somelists = [
            ['می\u200c', ''],
            ['کرد', 'رفت', 'شد'], 
            ['م', 'ی', 'یم','ید', 'ند', '']
        ]
        verbs = []
        for element in itertools.product(*somelists):
            verbs.append(''.join(element))

        if x[i] in verbs:
            if x[i].startswith('می'):
                x[i] = x[i][3:]
            if x[i].endswith('یم') or x[i].endswith('ید') or x[i].endswith('ند'):
                x[i] = x[i][:-2]
            if x[i].endswith('م') or x[i].endswith('ی'):
                x[i] = x[i][:-1]
    return x


frequent_words = ['.','در','از','،','؟','این','همین',':','که','است','در','می\u200cکردم', 'هم', 'او', 'و', 'وی', 'با', 'چه'
, 'اینکه', 'کنند', 'اگر', 'من', '!', '(', ')', 'س', 'را', 'بر', 'آن', 'نیز', 'ره', 'به', 'است', 'هست', 'یک', 'یا', 'برای'
, 'دیگر', 'بود', 'کسی', 'هر', '/'] 
## removing all one characters??? ! ? ( ) ع س : « » , ...
### what about numbers????
## نیروهای -  استانداردهای - 
# رسانه\u200cای
# واین 1
# اقتباس شده ۱
# کرده است ۱
# سده اخیر
# شناخته_شد 2 
# پرداخته_است 2


# 'رفتارهایی'
def delete_frequents(x, frequent_words):
    y = [w for w in x if w not in frequent_words] ## deleting frequent words
    return y


def add_word(doc_id, list_of_words, dic):
    for i in range(len(list_of_words)):
        position = i
        word = list_of_words[i]
        # print(word)
        if word not in dic:  ### if word is not in the dictionary
            dic[word] = [[doc_id, [i]]]
            # print('AAA')
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
                # print('BBB')
            else:   ### if word is occuring for the first time in this doc_id
                list_ = dic[word]
                list_.append([doc_id,[position]])
                dic[word] = list_
                # print('CCC')

    return dic





def give_dictionary():
    dic = {}
    # dfs = pd.read_excel('./../../News.xlsx')
    dfs = pd.read_excel('~/Codes/IR/Phase1/News.xlsx')
    
    contents = dfs['content']
    # doc_number = [i for i in range(10)]
    doc_number = [i for i in range(len(contents))]
    doc_number = list(set(doc_number) - set([1702, 1346, 1159, 1068, 1018, 907]))
    # indexes = [i for i in range(10)]

    for doc_id in doc_number:
        x = contents[doc_id]
        x = news_retrieval(x) # واکشی

        x = CaseFolding(x) # همسازی سازی

        # print(x)
        x = Normalizing(x)
        # print(x)
        x = Tokenization(x) # استخراج توکن
        # print(x)
        
        x = Stemming(x) ## ریشه یابی


        y = delete_frequents(x, frequent_words) # حذف پرتکرارها

        for i in range(len(y)):
            y[i] = re.sub(r'\u200c+', '\u200c', y[i])

        dic = add_word(doc_id, y, dic) # ایجاد شاخص معکوس مکانی
    
    return dic

dic = give_dictionary()
# import json
# with open('dic.txt', 'w') as file:
#     file.write(json.dumps(dic, ensure_ascii=False).encode('utf8').decode())



