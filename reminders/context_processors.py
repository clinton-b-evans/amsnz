from reminders.models import Notification


def user_notifications(request):
    print(request.user, 'user')
    notifications = Notification.objects.filter(reminder__user=request.user)
    unread_notifications = Notification.objects.filter(reminder__user=request.user, mark_read=False)
    unread = []
    for i in range(1, len(unread_notifications)):
        unread.append(unread_notifications[i])

    return {
        "unread": unread,
        "notifications": notifications,
        "length": len(notifications)
    }
