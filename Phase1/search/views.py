from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from .models import News


# Create your views here.
# class SearchView(TemplateView):
#     template_name = 'index.html'
query = None


def search(request):
    if not request.POST:
        # TODO: will be executed once
        # place of init process for posting list etc.

        return render(request, "index.html")
    elif request.POST["query"] == "":
        return render(request, "index.html")
    else:
        global query
        query = request.POST["query"]
        return redirect("news_list")


class NewsListView(ListView):
    model = News

    def get_queryset(self):
        # TODO: adjust doc_ids based on the query
        # doc_ids = foo(query)

        doc_ids = [1, 3, 5, 7]

        return News.objects.filter(doc_id__in=doc_ids).order_by("-publish_date")


class NewsDetailView(DetailView):
    model = News
