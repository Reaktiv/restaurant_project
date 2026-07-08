from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model

from notification.models import Notification

User = get_user_model()


@login_required
def notification_list(request):
    if request.user.role not in ['manager', 'admin']:
        return HttpResponseForbidden("Kirish huquqi yo'q")
    notifications = Notification.objects.all().order_by('is_Read')
    unread_count = notifications.filter(is_Read=False).count()

    context = {
        'notifications': notifications,
        'unread_count': unread_count
    }

    return render(request, 'notifications/reservation_notification.html', context=context)

@login_required
def mark_as_read(request, pk):
    if request.user.role not in ['manager', 'admin']:
        return HttpResponseForbidden("Kirish huquqi yo'q")
    notification = get_object_or_404(Notification, pk=pk)
    notification.is_Read = True
    notification.save()
    return redirect('notification_list')









