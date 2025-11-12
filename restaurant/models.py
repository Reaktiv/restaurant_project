from django.db import models
from account.models import CustomUser
from config.settings import AUTH_USER_MODEL

class Food(models.Model):
    TYPES = (
        ('Meal', 'Meal'),
        ('Drink', 'Drink'),
        ('Dessert', 'Dessert'),
        ('Seafood', 'Seafood'),
        ('Salads', 'Salads'),
        ('Healthy food', 'Healthy food'),
        ('Vegetarian', 'Vegetarian'),
        ('Icecream', 'Icecream'),
        ('FastFood', 'FastFood'),
    )

    added_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='foods')
    name_of_food = models.CharField(max_length=200)
    description = models.TextField(max_length=10000, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    type = models.CharField(max_length=50, choices=TYPES)

    def __str__(self):
        return self.name_of_food

class FoodImage(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='food_photos/')

    def __str__(self):
        return f"{self.food.name_of_food} rasmi"
