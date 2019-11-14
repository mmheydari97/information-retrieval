# from Input import parse_query
# from dictionary import give_dictionary


def words_query(word, dic): # returns doc_ids that include 'word'.  e.g. [1, 2]
    res = []
    if word in dic:
        docs = dic[word]
        for d in docs:
            res.append(d[0])    
    return res

# print(words_query('قرار', dic))


def postings(word, doc_id, dic): # returns position of 'word' in document=doc_id.  e.g. [1, 21, 59, 121]
    docs = dic[word]
    for d in docs:
        if d[0]==doc_id:
            return d[1]

# print(postings('گذشته', 0, dic))
# print(postings('گذشته', 1, dic))


def exact_query(exact, dic): # returns doc_ids that include the exact phrase. 
    words = exact.split(' ')
    docs = []
    for word in words:
        doc = words_query(word, dic)
        if(len(doc)==0): ## one word in phrase doesn't exit at all
            print('NOOOOOO')
            return []
        docs.append(doc)
    # print(docs)

    intersect = set(docs[0]).intersection(*docs) ## intersection of all postings lists
    # print(intersect) ## result is all docs that contain all words in "phrase"
    if len(intersect)==0:
        return []

    result = []
    for doc_id in intersect:
        positions = []
        for word in words:
            positions.append(postings(word, doc_id, dic))
        
        # print(positions)
        cnt = len(words) - 1
        for index in positions[0]:
            flag = True
            for i in range(cnt):
                if (index + i + 1) not in positions[i+1]:
                    flag = False
                    break
            if flag:
                result.append(doc_id)
            

    # print(result)
    return result


# exacts = ['رئیس هیأت امنای دفتر تبلیغات اسلامی']
# exacts = ['محمد گیلانی']
# exact_query(exacts[0], dic)

def result(words, exacts, nots, dic):

    if len(words)!=0:
        w_docs = words_query(words[0], dic)
        for word in words:
            tmp = words_query(word, dic)
            w_docs = list(set(w_docs) & set(tmp))
            if len(w_docs)==0:
                break
        
        if len(w_docs)==0:
            return []
    else:
        w_docs = "empty"
    


    if len(exacts)!=0:
        e_docs = exact_query(exacts[0], dic)
        for exact in exacts:
            tmp = exact_query(exact, dic)
            e_docs = list(set(e_docs) & set(tmp))
            if len(e_docs)==0:
                break
        
        if len(e_docs)==0:
            return []
    else:
        e_docs = "empty"

    
    n_docs = []
    for nott in nots:
        tmp = exact_query(nott, dic)
        n_docs = list(set(n_docs) & set(tmp))



    if e_docs=="empty" and w_docs=="empty":
        res = list(dic.keys()) ## all docs
        res = list(set(res) - set(n_docs))
        return res
    
    if e_docs=="empty":
        res = w_docs
        res = list(set(res) - set(n_docs))
        return res
    
    if w_docs=="empty":
        res = e_docs
        res = list(set(res) - set(n_docs))
        return res

    res = list(set(e_docs) & set(w_docs))
    res = list(set(res) - set(n_docs))

    return res

