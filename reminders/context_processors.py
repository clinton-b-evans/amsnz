from reminders.models import Notification


def user_notifications(request):
    print(request.user, 'user')
    notifications = Notification.objects.filter(reminder__user=request.user)
    return {
        "notifications": notifications,
        "length": len(notifications)
    }
