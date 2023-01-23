from datetime import date

from reminders.models import Reminder, Notification


def my_cron_job():
    print("executed")
    one_off_reminders = Reminder.objects.filter(due_date=date.today(), reminder_type="oneoff")
    for reminder in one_off_reminders:
        Notification.objects.get_or_create(date=date.today(), reminder=reminder)

    weekly_reminders = Reminder.objects.filter(due_date__week_day=date.today().weekday(), reminder_type="weekly")
    for reminder in weekly_reminders:
        Notification.objects.get_or_create(date=date.today(), reminder=reminder)

    monthly_reminders = Reminder.objects.filter(due_date__day=date.today().day, reminder_type="monthly")
    for reminder in monthly_reminders:
        Notification.objects.get_or_create(date=date.today(), reminder=reminder)

    yearly_reminders = Reminder.objects.filter(due_date__year=date.today().year, reminder_type="yearly")
    for reminder in yearly_reminders:
        Notification.objects.get_or_create(date=date.today(), reminder=reminder)