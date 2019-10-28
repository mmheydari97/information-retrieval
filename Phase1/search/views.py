from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import News


# Create your views here.
class SearchView(TemplateView):
    template_name = 'index.html'


class NewsListView(ListView):
    model = News

    def get_queryset(self):
        # TODO: adjust doc_ids based on the query
        doc_ids = [1, 3, 5, 7]

        return News.objects.filter(doc_id__in=doc_ids).order_by("-publish_date")


class NewsDetailView(DetailView):
    model = News
