# from sklearn.feature_extraction.text import TfidfVectorizer
from search.code.dictionary import give_dictionary, news_retrieval, Normalizing, \
    CaseFolding, Tokenization, remove_frequents, Stemming
# import pandas as pd
# from sklearn.metrics.pairwise import cosine_similarity
# import heapq


def preprocess(x):
    x = news_retrieval(x)
    x = Normalizing(x)
    x = CaseFolding(x)
    x = Tokenization(x)
    x = remove_frequents(x)
    x = Stemming(x)
    return x

#
# # def build_matrix():
# dic = give_dictionary()
# dic = dic.keys()
# # df = pd.read_excel("../../IR-F19-Project01-Input-2k.xlsx")
# df = pd.read_excel("IR-F19-Project01-Input-2k.xlsx")
# contents = df['content']
#
# # sublinear_tf is for 1+lg(tf)
# vec = TfidfVectorizer(analyzer=preprocess, vocabulary=dic, binary=False, sublinear_tf=True, use_idf=True)
# matrix = vec.fit_transform(contents)
#     # return matrix, vec
#
#
# # def find_similarity(matrix, vec, query):
# query = ["مجلس شورای اسلامی"]
# c = cosine_similarity(matrix, vec.transform(query))
# idx = heapq.nlargest(3, range(len(c)), c.take)
# for i in idx:
#     print(contents[i])
#     print()
#     print()
#     # return idx
#
#
# # if __name__ == "__main__":
# #     matrix, vec = build_matrix()
# #     idx = find_similarity(matrix, vec, query)
