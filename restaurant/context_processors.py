from notification.models import Notification

def notification_count(request):
    if request.user.is_authenticated and request.user.role in ['admin', 'manager']:
        return {
            'unread_count': Notification.objects.filter(is_Read=False).count()
        }
    return {
        'unread_count': 0
    }
