import json

from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from properties.models import Property
from reminders.models import Reminder
from django.db.models import Sum
from datetime import date, datetime
from .forms import ReminderForm

from datetime import datetime

# Create your views here.


def home_view(request):
    return render(request, "reminders/home.html", {})


def reminder_list_view(request):
    property=Property.objects.all()
    reminders = Reminder.objects.all().order_by("due_date")
    context = {
        "object_list": reminders,
        "property": property
    }
    return render(request, "reminders/main.html", context)


def addreminder(request):
    if request.method == "POST":
        print(request.body, "property")
        propertyData = json.loads(request.body)
        obj = Reminder.objects.create(
            property=Property.objects.get(name=propertyData["property"]),
            # property=propertyData["property"],
            detail=propertyData["detail"],
            due_date=propertyData["date"],
            reminder_type=propertyData["type"],
        )
        user = {
            'id': obj.id
        }
        data = {
            'user': user
        }
        print(data, 'data')
        return JsonResponse(data)


def editreminder(request):
    if request.method == "POST":
        print(request.body, "property")
        propertyData = json.loads(request.body)
        property = Reminder.objects.get(id=propertyData['id'])
        property.property = Property.objects.get(name=propertyData["property"])
        property.detail = propertyData['detail']
        property.reminder_type = propertyData['type']
        property.save()
        data = {
            'user': "data is updated"
        }
        return JsonResponse(data)


def deletereminder(request):
    id1 = request.GET.get('id', None)
    print(id1, "delete")
    Reminder.objects.get(id=id1).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)



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