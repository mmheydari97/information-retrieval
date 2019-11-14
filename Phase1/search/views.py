from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from .models import News
from .code.dictionary import give_dictionary
from .code.Input import parse_query, parse_query2
from .code.query import result, words_query, postings


# Create your views here.
# class SearchView(TemplateView):
#     template_name = 'index.html'
query = None
dic = {}


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
    model = News

    print('T1')
    global dic
    dic = give_dictionary()
    print('Dictionary Created')

    def get_queryset(self):
        # TODO: adjust doc_ids based on the query
        # doc_ids = foo(query)

        print('Query Recieved')
        # words, exacts, nots, source, cat = parse_query(query) ## or parse_query2
        words, exacts, nots, source, cat = parse_query2(query) ## or parse_query2
   
        doc_ids = result(words, exacts, nots, dic)
        # doc_ids = [1,2,3,4,5,6,7,8,9]

        return News.objects.filter(doc_id__in=doc_ids).order_by("-publish_date")


class NewsDetailView(DetailView):
    model = News
