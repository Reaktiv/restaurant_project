from django.urls import path
from reservations import views

urlpatterns = [
    path('table-create/', views.table_create, name='table_create'),
    path('make-reservation/', views.make_reservation, name='make_reservation'),
    path('all_tables/', views.all_tables, name='all_tables'),
    path('edit-table/<int:pk>/', views.edit_table, name='edit_table'),
    path('edit-reservation-table/<int:pk>/', views.edit_reservation_table, name='edit_reservation_table'),
]