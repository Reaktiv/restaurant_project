from django.urls import path
from reservations import views

urlpatterns = [
    path('table-create/', views.table_create, name='table_create'),
    path('make-reservation/', views.make_reservation, name='make_reservation'),
]