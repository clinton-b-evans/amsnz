from reminders.models import Notification


def user_notifications(request):
    if not request.user.is_anonymous:
        unread_notifications = Notification.objects.filter(reminder__user=request.user, mark_read=False)
        read_notifications = Notification.objects.filter(reminder__user=request.user, mark_read=True)
        notifications = []
        for i in range(0, len(unread_notifications)):
            notifications.append(unread_notifications[i])
        for i in range(0, len(read_notifications)):
            notifications.append(read_notifications[i])

        return {
            "unread": notifications,
            "notifications": notifications,
            "length": len(notifications)
        }
    else:
        return {
            "unread": [],
            "notifications": [],
            "length": 0
        }
