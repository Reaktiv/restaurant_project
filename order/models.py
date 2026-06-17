from django.db import models
from config.settings import AUTH_USER_MODEL
from reservations.models import Table
from restaurant.models import Food

User = AUTH_USER_MODEL

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='orders')
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, blank=True, null=True, related_name='table')
    waiter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='waiter_order')
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id} - Status: {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(Food, on_delete=models.PROTECT, related_name='food_item')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"#{self.order.id}. {self.food_item.name_of_food} ------ {self.order.status}"

