from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from reservations.forms import TableForm, ReservationsForm
from reservations.models import Reservations, Table


@login_required
def table_create(request):
    if request.user.role not in ['manager', 'admin']:
        return HttpResponseForbidden("Kirish huquqi yo'q")
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():

            form.save()
            return redirect('home')
    else:
        form = TableForm()

    return render(request, 'reservations/table_create.html', {'form': form})


@login_required
def make_reservation(request):
    if request.method == 'POST':
        form = ReservationsForm(request.POST)
        if form.is_valid():
            # 1. Tranzaksiya ichida ishlaymiz (bir vaqtda bitta stolni ikki kishi ololmasligi uchun)
            with transaction.atomic():
                reservation = form.save(commit=False)
                reservation.customer = request.user
                table = get_object_or_404(Table.objects.select_for_update(), id = reservation.table.id)
                table.is_active = False
                table.save()
                reservation.save()
            return redirect('home')
    else:
        form = ReservationsForm()

    context = {
        'form': form
    }

    return render(request, 'reservations/book_table.html', context=context)


@login_required
def all_tables(request):
    if request.user.role not in ['admin', 'manager']:
        return HttpResponseForbidden("Kirish huquqi yo'q")

    tables = Table.objects.all().order_by('number')
    is_active_count = tables.filter(is_active=True).count()
    context = {
        'all_tables': tables,
        'is_active_count': is_active_count
    }

    return render(request, 'reservations/all_tables.html', context=context)


@login_required
def edit_table(request, pk):
    if request.user.role not in ['manager', 'admin']:
        return HttpResponseForbidden("Kirish huquqi yo'q")
    table = get_object_or_404(Table, id=pk)
    if request.method == "POST":
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            return redirect('all_tables')
    else:
        form = TableForm(instance=table)

    context = {
        "form": form,
        "table": table
    }

    return render(request, 'reservations/edit_table.html', context=context)


@login_required
def edit_reservation_table(request, pk):

    if request.user.role not in ['manager', 'admin']:
        return HttpResponseForbidden("Kirish huquqi yo'q")

    reservation_table = get_object_or_404(Reservations, id=pk)
    old_table = reservation_table.table
    if request.method == "POST":
        form = ReservationsForm(request.POST, instance=reservation_table, users = request.user)
        if form.is_valid():
            new_reservation_form = form.save(commit=False)
            new_table = new_reservation_form.table
            if old_table != new_table:
                if old_table:
                    old_table.is_active = True
                    old_table.save()
                if new_table:
                    new_table.is_active = False
                    new_table.save()
            elif new_table:
                new_table.is_active = False
                new_table.save()
            new_reservation_form.save()
            form.save_m2m()
            return redirect('profile')
    else:
        form = ReservationsForm(instance=reservation_table, users=request.user)

    context = {
        'form': form
    }
    return render(request, 'reservations/edit_reservation_table.html', context=context)


@login_required
def reservation_tables(request):
    reservation_tables = Reservations.objects.filter(customer=request.user).select_related('table').order_by('date')
    if request.user.role in ['admin', 'manager']:
        reservation_tables = Reservations.objects.filter().select_related('table').order_by('date')

    context = {
        'reservation_tables': reservation_tables
    }

    return render(request, 'reservations/reservation_table.html', context=context)