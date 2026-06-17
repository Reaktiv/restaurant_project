from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render
from django.contrib.auth import get_user_model
from notification.models import Notification

from reservations.models import Reservations
User = get_user_model()

# Create your views here.

@receiver(post_save, sender=Reservations, dispatch_uid="unique_reservation_notification_signal")
def create_reservation_notification(sender, instance, created, **kwargs):
    if created:
             Notification.objects.create(
                 title=instance.customer.username,
                 message=f"Mijoz '{instance.customer.username}' tomonidan yangi stol buyurtmasi qabul qilindi. Sana: {instance.date}, Vaqt: {instance.time}."

             )