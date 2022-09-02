from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('order/', views.order, name='order'),
    path('receipt/', views.receipt, name='receipt'),
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.log_admin_out, name='admin_logout'),
    path('admincustomer/', views.admin, name='admin'),
    path('admincustomer/peabranch/<int:id>/', views.pea_editable, name='peaEditable'),
    path('admincustomer/peabranch/delete/<int:id>/', views.pea_delete, name='peaDelete'),
    path('admincustomer/product/<int:id>/', views.product_editable, name='productEditable'),
    path('admincustomer/product/delete/<int:id>/', views.product_delete, name='productDelete'),
    path('admincustomer/order/<int:id>/', views.order_editable, name='orderEditable'),
    path('admincustomer/order/delete/<int:id>/', views.order_delete, name='orderDelete'),
    path('admincustomer/receipt/<int:id>/', views.receipt_editable, name='receiptEditable'),
    path('admincustomer/receipt/delete/<int:id>/', views.receipt_delete, name='receiptDelete'),
]
