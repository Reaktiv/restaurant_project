
from django.db.models import Q
from django.http import HttpResponseBadRequest, HttpResponseForbidden

from notification.models import Notification
from reservations.forms import ReservationsForm
from restaurant.models import Food, Favourite
from django.shortcuts import render, get_object_or_404, redirect
from restaurant.forms import FoodForm
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home(request):
    search_food = request.GET.get('search_published_foods')
    if search_food:
        foods = Food.objects.filter(
            Q(name_of_food__icontains=search_food) | Q(description__icontains=search_food),
            published=True).order_by('?')[:8]
    else:
        foods = Food.objects.filter(published=True).order_by('?')[:8]

    if request.method == 'POST':
        form = ReservationsForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.customer = request.user
            reservation.save()
            return redirect('home')
    else:
        form = ReservationsForm()

    notifications = Notification.objects.all().order_by('-created_at')
    unread_count = notifications.filter(is_Read=False).count()

    context = {
        'foods': foods,
        'unread_count':unread_count,
        'form': form

    }

    return render(request, 'restaurant/home.html', context=context)


def detail(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    foods = Food.objects.filter(published=True, type=food.type)

    context = {
        'food': food,
        'foods': foods,
    }
    return render(request, 'restaurant/detail.html', context=context)


def update(request, food_id):
    role = request.user.role
    if role not in ['admin', 'manager']:
        return HttpResponseForbidden("Kirish huquqi yo'q")


    food = get_object_or_404(Food, id=food_id)
    if request.user.is_superuser and request.user.is_staff:
        user_perm = False
    else:
        user_perm = True
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
        'user_perm': user_perm
    }
    return render(request, 'restaurant/update.html', context=context)


def delete(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    food.delete()
    return redirect('home')


@login_required
def create(request):
    role = request.user.role
    if role not in ['admin', 'manager']:
        return HttpResponseForbidden("Kirish huquqi yo'q")
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            food = form.save(commit=False)
            food.added_by = request.user
            food.save()
            return redirect('food_page')
    else:
        form = FoodForm()

    return render(request, 'restaurant/create.html', {'form': form,
                                                                           'role': role})

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


def cart(request):
    basket = request.session.get('basket', {})

    food_ids = [key for key in basket.keys() if key.isdigit()]
    foods = Food.objects.filter(id__in=food_ids).select_related()
    favourite_foods = Food.objects.filter(favourite_by__user=request.user)
    basket_items = []
    total_price = 0

    for food in foods:
        quantity = int(basket[str(food.id)])
        basket_items.append({
            'food': food,
            'quantity': quantity,
            'total': food.price * quantity
        })
        total_price += food.price * quantity
    context = {
        'basket_items': basket_items,
        'total_price': total_price,
        'favourite_foods': favourite_foods,
    }

    return render(request, 'restaurant/cart.html', context=context)


def cart_add(request, food_id):
    if request.method == 'POST':
        try:
            Food.objects.get(id=food_id)
            basket = request.session.get('basket', {})
            basket[str(food_id)] = basket.get(str(food_id), 0) + 1
            request.session['basket'] = basket
            request.session.modified = True
        except Food.DoesNotExist:
            pass
        return redirect('food_page')
    return HttpResponseBadRequest("Invalid request method")


def cart_remove(request, food_id):
    basket = request.session.get('basket', {})
    food_id_str = str(food_id)

    if food_id_str in basket:
        quantity = int(basket[food_id_str])
        if quantity > 1:
            basket[food_id_str] = quantity - 1  # Miqdorni 1 taga kamaytir
        else:
            del basket[food_id_str]  # Agar 1 bo‘lsa va kamaytirilsa, o‘chirib yubor

        request.session['basket'] = basket
        request.session.modified = True  # Sessiyani yangilash

    return redirect('cart')


def payment(request):
    return HttpResponseBadRequest("To'landi😁")


@login_required()
def add_favourite(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    Favourite.objects.get_or_create(user=request.user,
                                    food=food)

    return redirect(request.META.get('HTTP_REFERER'))

@login_required()
def remove_favourite(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    Favourite.objects.filter(user=request.user, food=food).delete()

    return redirect(request.META.get('HTTP_REFERER'))






































