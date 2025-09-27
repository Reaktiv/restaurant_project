import random
from restaurant.models import Food
from django.shortcuts import render

# Create your views here.

def home(request):
    foods = Food.objects.filter()

    context = {
        'foods': foods,

    }

    return render(request, 'restaurant/home.html', context=context)



