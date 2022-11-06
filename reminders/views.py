import json

from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from properties.models import Property
from reminders.models import Reminder
from django.db.models import Sum
from datetime import date, datetime
from .forms import ReminderForm

# Create your views here.


def home_view(request):
    return render(request, "reminders/home.html", {})


def reminder_list_view(request):
    reminders = Reminder.objects.all().order_by("due_date")
    context = {
        "object_list": reminders,
    }
    return render(request, "reminders/main.html", context)


def add_reminder(request):
    submitted = False
    if request.method == "POST":
        form = ReminderForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    else:
        form = ReminderForm
        if "submitted" in request.GET:
            submitted = True
    form = ReminderForm
    return render(
        request, "reminders/add_reminders.html", {"form": form, "submitted": submitted}
    )


def update_reminder(request, pk):
    reminder = Reminder.objects.get(id=pk)
    form = ReminderForm(instance=reminder)

    if request.method == "POST":
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    context = {"form": form}
    return render(request, "reminders/add_reminders.html", context)


def delete_reminder(request, pk):
    reminder = Reminder.objects.get(id=pk)
    qs = Reminder.objects.get(id=pk)
    context = {
        "object": qs,
    }

    if request.method == "POST":
        reminder.delete()
        return HttpResponse('<script type="text/javascript">window.close()</script>')
    return render(request, "reminders/delete.html", context)


def get_reminders(request):
    reminders = Reminder.objects.filter(due_date__gte=date.today())
    reminder_list = []
    for reminder in reminders:
        if reminder.reminder_type == "oneoff":
            if reminder.due_date == date.today():
                reminder_list.append({
                    "detail": reminder.detail,
                    "reminder_type": reminder.reminder_type,
                    "property": reminder.property.name,
                }
                )
        elif reminder.reminder_type == "weekly":
            pass
        elif reminder.reminder_type == "bi-weekly":
            pass
        elif reminder.reminder_type == "monthly":
            pass
        elif reminder.reminder_type == "yearly":
            pass
        elif reminder.reminder_type == "quarterly":
            pass
    return HttpResponse(serializers.serialize('json', reminders), content_type="application/json")