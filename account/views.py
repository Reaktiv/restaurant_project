
from django.shortcuts import render, redirect

from account.forms import CustomUserCreationForm, CustomUserChangeForm, ProfileChangeForm
from order.models import Order
from reservations.models import Reservations
from restaurant.models import Food
from .models import Profile

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'account/register.html', context=context)

def profile(request):
    favourite_foods = Food.objects.filter(favourite_by__user=request.user)
    reservation_tables = Reservations.objects.filter(customer=request.user).select_related('table').order_by('-date', '-time')
    all_reservation_tables = Reservations.objects.filter().select_related('table').order_by('-date', '-time')
    old_orders = Order.objects.filter(is_paid=True, customer=request.user).prefetch_related('items')

    role = request.user.role
    if role in ['manager', 'admin']:
        reservation_tables = all_reservation_tables
    context = {
        "foods": favourite_foods,
        'reservation_tables': reservation_tables,
        'old_orders': old_orders,
    }
    return render(request, 'account/profile.html', context=context)

def change_profile(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileChangeForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    else:
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = ProfileChangeForm(instance=profile)

    context = {
        'u_form': user_form,
        'p_form': profile_form,
    }

    return render(request, 'account/change_profile.html', context)

def password_reset(request):
    pass
