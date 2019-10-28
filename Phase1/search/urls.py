from django.urls import path
from search import views


urlpatterns = [
    path('', views.SearchView.as_view(), name="search"),
    path("q", views.NewsListView.as_view(), name="news_list"),
    path(r'news/(?P<pk>\d+)', views.NewsDetailView.as_view(), name='news_detail'),
]
