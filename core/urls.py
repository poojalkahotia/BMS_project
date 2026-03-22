from django.urls import path
from . import views_global_search

urlpatterns = [
    path('search/', views_global_search.global_search, name='global_search'),
]
