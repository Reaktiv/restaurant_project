from django.contrib.auth import views as auth_views
from account import views as account_views
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'),
         name='login'
         ),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/login.html'),
         name='logout'),
    path('register/', account_views.register, name='register'),
    path('profile/', account_views.profile, name='profile'),
    path('change_profile/', account_views.change_profile, name='change_profile'),
    path('password/', auth_views.PasswordResetView.as_view(
        template_name='account/password_reset.html',
        success_url=reverse_lazy('password_reset_done')),
         name='password_reset'
         ),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'
    ),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_confirm.html'
    ),
         name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'
    ),
         name='password_reset_complete'),

]
