from django.urls import path
from . import views

urlpatterns = [
    path('sale/entry/', views.sale_entry, name='sale_entry'),
    path('sale/edit/<str:pk>/', views.sale_entry, name='sale_edit'),
    path('sale/save/', views.save_sale, name='save_sale'),
    path('sale/list/', views.sale_list, name='sale_list'),
    
    path('purchase/entry/', views.purchase_entry, name='purchase_entry'),
    path('purchase/edit/<str:pk>/', views.purchase_edit, name='purchase_edit'),
    path('purchase/save/', views.save_purchase, name='save_purchase'),
    path('purchase/list/', views.purchase_list, name='purchase_list'),
    path('receipt/entry/', views.receipt_entry, name='receipt_entry'),
    path('receipt/edit/<str:pk>/', views.receipt_entry, name='receipt_edit'),
    path('receipt/save/', views.save_receipt, name='save_receipt'),
    path('receipt/delete/<str:pk>/', views.delete_receipt, name='delete_receipt'),
    path('receipt/list/', views.receipt_list, name='receipt_list'),
    path('payment/entry/', views.payment_entry, name='payment_entry'),
    path('payment/edit/<str:pk>/', views.payment_entry, name='payment_edit'),
    path('payment/save/', views.save_payment, name='save_payment'),
    path('payment/delete/<str:pk>/', views.delete_payment, name='delete_payment'),
    path('payment/list/', views.payment_list, name='payment_list'),
    path('party-ledger/', views.party_ledger, name='party_ledger'),
    path('party-balance/', views.party_balance_list, name='party_balance_list'),
    path('current-stock/', views.current_stock_report, name='current_stock_report'),
    path('item-ledger/', views.item_ledger, name='item_ledger'),
]
