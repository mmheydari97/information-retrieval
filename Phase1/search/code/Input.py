import re
import itertools
from dictionary import news_retrieval, Normalizing, CaseFolding, Tokenization, remove_frequents, Stemming

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
 
    word_preprocessor, not_processor = '', ''
    for ww in words:
        word_preprocessor += ww + ' '
    words = Stemming(remove_frequents(Tokenization(CaseFolding(Normalizing(news_retrieval(word_preprocessor.strip()))))))
    # print(words)
     
    for ww in nots:
        not_processor += ww + ' '
    nots = Stemming(remove_frequents(Tokenization(CaseFolding(Normalizing(news_retrieval(not_processor.strip()))))))
    # print(nots)

    ex_tmp = []
    for e in exacts:
        ee = Stemming(remove_frequents(Tokenization(CaseFolding(Normalizing(news_retrieval(e.strip()))))))
        eee = ''
        for ww in ee:
            eee += ww + ' '
        ex_tmp.append(eee.strip())
    exacts = ex_tmp
    # print(exacts)

    return words, exacts, nots, source, cat


# # input = '"بازیابی اطلاعات" امیرکبیر !درس پسرها درختان شدم !رفتم'
# # input = '"بازیابی اطلاعات" امیرکبیر !درس پسرها درختان شدم !رفتم cat:ورزش'
# # input = '"سیستان و بلوچستان"'
# input = '"بازیابی می سی سی پی" امپراطور !درس؟ کتاب ها گفت و گو درختان. "آقایان و خانم‌ ها" مي رفتم !رفتم cat:ورزش'
# words, exacts, nots, source, cat = parse_query2(input)
# # words, exacts, nots, source, cat = parse_query(input)
# print(words)
# print(exacts)
# print(nots)
# print(source)
# print(cat)

