from django.urls import path
from . import views

urlpatterns = [
    path('party/add/', views.party_create, name='party_create'),
    path('party/update/<str:pk>/', views.party_update, name='party_update'),
    path('party/delete/<str:pk>/', views.party_delete, name='party_delete'),
    path('party/list/', views.party_list, name='party_list'),
    path('item/add/', views.item_create, name='item_create'),
    path('item/update/<str:pk>/', views.item_update, name='item_update'),
    path('item/delete/<str:pk>/', views.item_delete, name='item_delete'),
    path('item/list/', views.item_list, name='item_list'),
    path('company/add/', views.company_create, name='company_create'),
    path('company/delete/<str:pk>/', views.company_delete, name='company_delete'),
    path('category/add/', views.category_create, name='category_create'),
    path('category/delete/<str:pk>/', views.category_delete, name='category_delete'),
    path('api/party-details/', views.get_party_details, name='get_party_details'),
    path('api/item-details/', views.get_item_details, name='get_item_details'),
]
