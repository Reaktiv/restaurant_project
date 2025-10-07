import random

from django.db.models import Q
from config.settings import AUTH_USER_MODEL
from restaurant.models import Food
from django.shortcuts import render, get_object_or_404, redirect
from restaurant.forms import FoodForm
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home(request):
    search_food = request.GET.get('search_published_foods')
    if search_food:
        foods = Food.objects.filter(
            Q(name_of_food__icontains=search_food) | Q(description__icontains=search_food), published=True).order_by(
            '?')[:8]
    else:
        foods = Food.objects.filter(published=True).order_by('?')[:8]

    context = {
        'foods': foods,

    }

    return render(request, 'restaurant/home.html', context=context)


def detail(request, food_id):
    food = get_object_or_404(Food, id=food_id)

    context = {
        'food': food,
    }
    return render(request, 'restaurant/detail.html', context=context)


def update(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FoodForm(instance=food)
    context = {
        'form': form,
        'food': food,
    }
    return render(request, 'restaurant/update.html', context=context)


def delete(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    food.delete()
    return redirect('home')


@login_required
def create(request):
    if request.method == "POST":
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            food = form.save(commit=False)
            food.added_by = request.user
            food.save()
            return redirect('home')
    else:
        form = FoodForm()
    context = {
        'form': form,
    }
    return render(request, 'restaurant/create.html', context=context)


def food_page(request):
    foods = Food.objects.filter(published=True)

    context = {
        'foods': foods,
    }
    return render(request, 'restaurant/foods_page.html', context=context)

def by_category(request, food_type):
    foods = Food.objects.filter(published=True, type=food_type)

    context = {
        'foods': foods,
        'type': food_type
    }
    return render(request, 'restaurant/by_category.html', context=context)

