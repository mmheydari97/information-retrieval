from django.urls import path, re_path
from search import views


urlpatterns = [
    # path('', views.SearchView.as_view(), name="search"),
    path('', views.search, name="search"),
    path("news", views.NewsListView.as_view(), name="news_list"),
    re_path(r'news/(?P<pk>\d+)', views.NewsDetailView.as_view(), name='news_detail'),
]
