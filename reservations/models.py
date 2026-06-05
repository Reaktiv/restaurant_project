from django.db import models

from config import settings
from config.settings import AUTH_USER_MODEL


class Table(models.Model):
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField(verbose_name='Capacity')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.number} - table. Capacity - {self.capacity}"


class Reservations(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    name = models.CharField(max_length=50, null=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.PositiveIntegerField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.customer.username} - {self.date} {self.time}"


