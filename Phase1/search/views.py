from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from .models import News
from .code.dictionary import give_dictionary
from .code.Input import parse_query, parse_query2
from .code.query import result, words_query, postings
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import heapq
from search.code.tfidf import preprocess


# Create your views here.
# class SearchView(TemplateView):
#     template_name = 'index.html'
query = None
dic = {}
matrix = None
vec = None


def search(request):
    if not request.POST:
        # TODO: will be executed once
        # place of init process for posting list etc.
        
        print('A1')

        return render(request, "index.html")
    elif request.POST["query"] == "":
        print('Empty Input!!!')

        return render(request, "index.html")
    else:
        print('C3')

        global query
        query = request.POST["query"]

        return redirect("news_list")


class NewsListView(ListView):
    paginate_by = 5
    model = News
    extra_context = {"highlights": ["روز","مجلس","حسین"]}
    print('T11')
    global dic
    global matrix
    global vec
    df = pd.read_csv("IR-F19-Project02-14k.csv")
    contents = df['content']

    dic = give_dictionary()
    print('Dictionary Created')
    dict = dic.keys()
    # # print(dic)
    # # print("content: ", type(contents))
    vec = TfidfVectorizer(analyzer=preprocess, vocabulary=dict, binary=False, sublinear_tf=True, use_idf=True)
    matrix = vec.fit_transform(contents)
    # # print("-------------------")
    # print(matrix is None)
    # print("-------------------")

    def get_queryset(self):
        # TODO: adjust doc_ids based on the query
        # doc_ids = foo(query)

        print('Query Recieved')
        # words, exacts, nots, source, cat = parse_query(query) ## or parse_query2
        words, exacts, nots, source, cat = parse_query2(query) ## or parse_query2

        tfidf_input = ''
        for ww in words:
            tfidf_input += ww + ' '
        tfidf_input = tfidf_input.strip()
        tfidf_input = [tfidf_input]
        # for ex in exacts:
        #     tfidf_input += ex + " "

        c = cosine_similarity(matrix, vec.transform(tfidf_input))
        idx = heapq.nlargest(30, range(len(c)), c.take)

        # print("==========================================================")
        # for i in idx:
        #     print(c[i])
        # print("==========================================================")

        # print(tfidf_input)

        doc_ids = result(words, exacts, nots, dic)
        # doc_ids = range(20)
        if tfidf_input[0] == "":
            return News.objects.filter(doc_id__in=doc_ids).order_by("-publish_date")

        a = News.objects.filter(doc_id__in=idx).intersection(News.objects.filter(doc_id__in=doc_ids))

        return a


class NewsDetailView(DetailView):
    model = News
