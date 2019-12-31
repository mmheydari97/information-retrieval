from builtins import super
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import News
from .code.dictionary import give_dictionary
from .code.Input import parse_query, parse_query2
from .code.query import result
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import heapq
from search.code.tfidf import preprocess


query = None
dic = {}
matrix = None
vec = None


def search(request):
    if not request.POST:
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
    print('T11')
    global dic
    global matrix
    global vec
    df = pd.read_csv("IR-F19-Project02-14k.csv")[:1000]
    contents = df['content']

    dic = give_dictionary()
    print('Dictionary Created')
    dict = dic.keys()

    vec = TfidfVectorizer(analyzer=preprocess, vocabulary=dict, binary=False, sublinear_tf=True, use_idf=True)
    matrix = vec.fit_transform(contents)

    def get_queryset(self):

        print('Query Recieved')
        # words, exacts, nots, source, cat = parse_query(query) ## or parse_query2
        words, exacts, nots, source, cat = parse_query2(query) ## or parse_query2

        tfidf_input = ''
        for ww in words:
            tfidf_input += ww + ' '
        tfidf_input = tfidf_input.strip()
        tfidf_input = [tfidf_input]

        c = cosine_similarity(matrix, vec.transform(tfidf_input))
        idx = heapq.nlargest(30, range(len(c)), c.take)

        doc_ids = result(words, exacts, nots, dic)
        if tfidf_input[0] == "":
            return News.objects.filter(doc_id__in=doc_ids).order_by("-publish_date")

        a = News.objects.filter(doc_id__in=idx).intersection(News.objects.filter(doc_id__in=doc_ids))

        return a


class NewsDetailView(DetailView):

    model = News

    def get_queryset(self):
        words, exacts, nots, source, cat = parse_query2(query)
        self.extra_context = {"words": words}
        return super(NewsDetailView, self).get_queryset()

