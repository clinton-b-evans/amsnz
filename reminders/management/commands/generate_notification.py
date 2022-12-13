from datetime import date

from django.core.management.base import BaseCommand, CommandError

from reminders.models import Reminder, Notification


class Command(BaseCommand):
    help = 'Generate notification'


    def handle(self, *args, **options):
        try:
            one_off_reminders = Reminder.objects.filter(due_date=date.today(), reminder_type="oneoff")
            for reminder in one_off_reminders:
                notification , created = Notification.objects.get_or_create(date=date.today(), reminder=reminder)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Notification added for {reminder.user.username}"))

            weekly_reminders = Reminder.objects.filter(due_date__week_day=date.today().weekday(), reminder_type="weekly")
            for reminder in weekly_reminders:
                notification , created = Notification.objects.get_or_create(date=date.today(), reminder=reminder)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Notification added for {reminder.user.username}"))

            monthly_reminders = Reminder.objects.filter(due_date__day=date.today().day, reminder_type="monthly")
            for reminder in monthly_reminders:
                notification , created = Notification.objects.get_or_create(date=date.today(), reminder=reminder)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Notification added for {reminder.user.username}"))

            yearly_reminders = Reminder.objects.filter(due_date__year=date.today().year, reminder_type="yearly")
            for reminder in yearly_reminders:
                notification , created = Notification.objects.get_or_create(date=date.today(), reminder=reminder)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Notification added for {reminder.user.username}"))
        except Exception as err:
            self.stdout.write(self.style.SUCCESS(f"{err}"))