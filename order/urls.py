from django.urls import path
from order import views

urlpatterns = [
    path('waiter-create-order/', views.waiter_create_order, name='waiter_create_order'),
    path('all-orders/', views.all_orders, name='all_orders'),
    path('customer-create-orders/', views.customer_create_order, name='customer_create_order'),
    path('order-detail/<int:pk>', views.order_detail, name='order_detail'),
    path('edit-order/<int:pk>', views.edit_order, name='edit_order'),
]