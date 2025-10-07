from restaurant import views
from django.urls import path


urlpatterns = [
    path('',views.home, name='home'),
    path('<int:food_id>/detail',views.detail, name='detail'),
    path('<int:food_id>/update', views.update, name='update'),
    path('<int:food_id>/delete', views.delete, name='delete'),
    path('create/', views.create, name='create'),
    path('food_page/', views.food_page, name='food_page'),
    path('<str:food_type>by_category/', views.by_category, name='by_category')
]