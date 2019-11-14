import re
from hazm import *
import itertools

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

        # تشنگان گرسنگان ستارگان نویسندگان شنوندگان چوگان زندگان آسودگان 
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
, 'اینکه', 'کنند', 'اگر', 'من', '(', ')', 'س', 'را', 'بر', 'آن', 'نیز', 'ره', 'به', 'است', 'هست', 'یک', 'یا', 'برای'
, 'دیگر', 'بود', 'کسی', 'هر', '/'] # ! and " should not be removed 

def delete_frequents(x, frequent_words):
    y = [w for w in x if w not in frequent_words] ## deleting frequent words
    return y




def find(input, phrase): ## phrase must be 'cat' or 'source'
    result = ""
    start = input.find(phrase+':')
    if input.find(phrase+':')!=-1:
        index = start
        index += len(phrase + ':') #7=length of source: / 4=length of cat:
        if(input[index]==' '): # if there is a space between : and source/cat keyword
            index+=1
        end = index
        while(end!=len(input) and input[end]!=' '): # note that end!=length must be checked first(To prevent OutOfRange error)
            end+=1
        result = input[index:end]
        input = input[0:start] + input[end:] # omitting phrase
    return input, result



def give_input(input):
    exacts = []
    words = []
    source = "" # must be one word. e.g. source:times 
    cat = "" # likewise

    input, source = find(input, 'source')
    input, cat = find(input, 'cat')

    input = input.strip()
    length = len(input)
    index = 0
    exacts = re.findall('"(.*?)"', input) # all phrases in quotation

    for w in exacts: # remove all exacts
        start = input.find(w)
        end = start + len(w)
        input = input[0:start-1] + input[end+1:]

    input = ' '.join(input.split()) # Substitute multiple whitespace with single whitespace
    words = input.split(' ') ## find all tokens

    return words, exacts, source, cat





def parse_query(input):

    ### interpreting the input.
    nots = []
    words = []

    word, exacts, source, cat = give_input(input)

    nots = []
    words = []

    if not(len(word)==1 and word[0]==''): ## if word is not empty (word=[''])
        for w in word:
            if w[0]=='!':
                nots.append(w[1:])
            else:
                words.append(w)

    return words, exacts, nots, source, cat


def parse_query2(input):

    nots = []
    words = []

    word, exacts, source, cat = give_input(input)

    nots = []
    words = []

    if not(len(word)==1 and word[0]==''):
        for w in word:
            if w[0]=='!':
                nots.append(w[1:])
            else:
                words.append(w)

    words = Stemming(words)
    tmp = []
    for x in words:
        x = CaseFolding(x)
        if x not in frequent_words:
            tmp.append(x)
    words = tmp
    
    nots = Stemming(nots)
    tmp = []
    for x in nots:
        x = CaseFolding(x)
        if x not in frequent_words:
            tmp.append(x)
    nots = tmp


    for i in range(len(exacts)):
        phrase = exacts[i]
        phrase = CaseFolding(phrase)

        res = ''
        w = phrase.split(' ')
        w = Stemming(w)
    
        for ww in w:
            if ww in frequent_words:
                ww = ''
            res += ww + ' '

        exacts[i] = res.strip()


    return words, exacts, nots, source, cat


