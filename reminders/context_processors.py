from reminders.models import Notification


def user_notifications(request):
    if request.user.is_anonymous():
        notifications = Notification.objects.filter(reminder__user_id=request.user)
        unread_notifications = Notification.objects.filter(reminder__user=request.user, mark_read=False)
        unread = []
        for i in range(1, len(unread_notifications)):
            unread.append(unread_notifications[i])

        return {
            "unread": unread,
            "notifications": notifications,
            "length": len(notifications)
        }
    else:
        return {
            "unread": [],
            "notifications": [],
            "length": 0
        }

