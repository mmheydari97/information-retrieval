from django.urls import path
from search import views


urlpatterns = [
    path('', views.SearchView.as_view(), name="search"),
]
