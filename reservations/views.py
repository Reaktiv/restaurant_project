from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from reservations.forms import TableForm, ReservationsForm
from reservations.models import Reservations


@login_required
def table_create(request):
    role = request.user.role
    if role not in ['manager', 'admin']:
        return HttpResponseForbidden("Kirish huquqi yo'q")
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TableForm()

    return render(request, 'reservations/table_create.html', {'form': form})


def make_reservation(request):
    if request.method == 'POST':
        form = ReservationsForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.customer = request.user
            reservation.save()
            return redirect('home')
    else:
        form = ReservationsForm()

    return render(request, 'reservations/book_table.html', context={'form': form})














