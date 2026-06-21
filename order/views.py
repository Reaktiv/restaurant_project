from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from order.forms import OrderItemForm, OrderForm, OrderFormSet
from order.models import Order, OrderItem
from reservations.models import Table
from restaurant.models import Food


@login_required
def customer_create_order(request):
    basket = request.session.get('basket', {})

    if not basket:
        return redirect('cart')

    if request.method == 'POST':
        table_id = request.POST.get('table')
        table = get_object_or_404(Table, id=table_id)

        order = Order.objects.create(
            customer=request.user,
            table=table,
            status='pending',
            waiter=None
        )

        total_summa = 0
        food_ids = [key for key in basket.keys() if key.isdigit()]
        foods = Food.objects.filter(id__in=food_ids)

        for food in foods:
            quantity = int(basket[str(food.id)])
            item_price = food.price

            OrderItem.objects.create(
                order=order,
                food_item=food,
                quantity=quantity,
                price=item_price
            )
            total_summa += item_price * quantity

        order.total_price = total_summa
        order.is_paid = True
        order.save()
        table.is_active = False
        table.save()
        if 'basket' in request.session:
            del request.session['basket']
            request.session.modified = True

        return redirect('home')

    active_tables = Table.objects.filter(is_active=True)

    food_ids = [key for key in basket.keys() if key.isdigit()]
    foods = Food.objects.filter(id__in=food_ids)

    basket_items = []
    total_price = 0
    for food in foods:
        quantity = int(basket[str(food.id)])
        item_total = food.price * quantity
        total_price += item_total
        basket_items.append({
            'food': food,
            'quantity': quantity,
            'total': item_total
        })

    context = {
        'tables': active_tables,
        'basket_items': basket_items,
        'total_price': total_price
    }
    return render(request, 'orders/customer_create_order.html', context=context)


def waiter_create_order(request):
    role = request.user.role
    if role not in ['admin', 'manager', 'waiter']:
        return HttpResponseForbidden("Kirish huquqi yo'q")

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST)
        if order_form.is_valid() and formset.is_valid():
            order = order_form.save(commit=False)
            if request.user.role == 'waiter':
                order.waiter = request.user
            else:
                order.customer = request.user
            order.table.is_active = False
            order.table.save()
            order.is_paid = True
            order.save()

            formset.instance = order
            order_items = formset.save(commit=False)

            total_summa = 0
            for item in order_items:
                item.price = item.food_item.price
                total_summa += item.price * item.quantity
                item.save()

            order.total_price = total_summa
            order.save()
            return redirect('cart')
    else:
        order_form = OrderForm()
        formset = OrderFormSet()

        context = {
            'order_form': order_form,
            'formset': formset,
        }
        return render(request, 'orders/waiter_create_order.html', context=context)


def all_orders(request):
    role = request.user.role
    if role not in ['admin', 'manager', 'waiter']:
        return HttpResponseForbidden("Kirish huquqi yo'q")

    all_orders = Order.objects.filter(status__in=['pending', 'ready', 'preparing']).prefetch_related('items').order_by('-created_at')
    context = {
        "all_orders": all_orders,
    }
    return render(request, 'orders/all_orders.html', context=context)


def order_detail(request, pk):
    order = get_object_or_404(Order.objects.all().prefetch_related('items'), id=pk)
    context = {
        'order': order,
        'order_items': order.items.all()
    }
    return render(request, 'orders/order_detail.html', context=context)


def edit_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    old_table = order.table
    if request.method == "POST":
        order_form = OrderForm(request.POST, instance=order)
        formset = OrderFormSet(request.POST, instance=order)
        if order_form.is_valid() and formset.is_valid():
            order = order_form.save()

            order_items = formset.save(commit=False)
            total_summa = 0
            for item in order_items:
                item.price = item.food_item.price
                total_summa += item.price * item.quantity
                item.save()
            formset.save_m2m()
            order.total_price = total_summa
            new_table = order.table
            if old_table != new_table:
                old_table.is_active = True
                old_table.save()
                order.table.is_active = False
                order.table.save()
            order.save()
            return redirect('home')
    else:
        order_form = OrderForm(instance=order)
        formset = OrderFormSet(instance=order)

    context = {
        'order_form': order_form,
        'formset': formset,
        'order': order
    }
    return render(request, 'orders/edit_order.html', context=context)
