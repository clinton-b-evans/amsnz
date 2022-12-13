import json

from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from incomestatements_property.views import sort_years_list
from properties.models import Property
from reminders.models import Reminder, Notification
from django.db.models import Sum
from datetime import date, datetime
from .forms import ReminderForm

from datetime import datetime


# Create your views here.


def home_view(request):
    return render(request, "reminders/home.html", {})


def notifications_view(request):
    return render(request, "reminders/notifications.html")


def update_notifications(request, id):
    print(request, 'id=>', id)
    notification = Notification.objects.get(id=id)
    if notification.mark_read:
        notification.mark_read = False
    else:
        notification.mark_read = True
    notification.save()
    print(notification.mark_read, 'mark')
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "transactionListChanged": None,
                "showMessage": f"{notification} updated."
            })
        }
    )


def notifications_list(request):
    unread_notifications = Notification.objects.filter(reminder__user=request.user, mark_read=False)
    read_notifications = Notification.objects.filter(reminder__user=request.user, mark_read=True)
    notifications = []
    for i in range(0, len(unread_notifications)):
        notifications.append(unread_notifications[i])
    for i in range(0, len(read_notifications)):
        notifications.append(read_notifications[i])
    notifications_to_show = []
    loop = 0
    for i in range(0, len(notifications)):
        if loop < 5:
            notifications_to_show.append(notifications[i])
        loop += 1
        print('index', i)
    context = {
        "unread": notifications,
        "notifications": notifications,
        "length": len(notifications),
        "notifications_to_show": notifications_to_show
    }
    return render(request, 'reminders/notifications_list.html', context=context)


def notifications_table_list(request):
    unread_notifications = Notification.objects.filter(reminder__user=request.user, mark_read=False)
    read_notifications = Notification.objects.filter(reminder__user=request.user, mark_read=True)
    notifications = []
    for i in range(0, len(unread_notifications)):
        notifications.append(unread_notifications[i])
    for i in range(0, len(read_notifications)):
        notifications.append(read_notifications[i])
    context = {
        "unread": notifications,
        "notifications": notifications,
        "length": len(notifications)
    }
    return render(request, 'reminders/table_data.html', context=context)


def reminder_list_view(request, year):
    property = Property.objects.filter(user=request.user)
    reminders = Reminder.objects.filter(user=request.user).order_by("due_date")
    years = Reminder.objects.filter(user=request.user).values_list("due_date__year").distinct()
    years_list = []
    for data in years:
        for item in data:
            years_list.append(item)
    years_list = sort_years_list(years_list)
    context = {
        "object_list": reminders,
        "property": property,
        "years_list": years_list
    }
    return render(request, "reminders/main.html", context)


def addreminder(request):
    if request.method == "POST":
        print(request.body, "property")
        propertyData = json.loads(request.body)
        obj = Reminder.objects.create(
            property=Property.objects.filter(user=request.user).get(name=propertyData["property"]),
            # property=propertyData["property"],
            detail=propertyData["detail"],
            due_date=propertyData["date"],
            reminder_type=propertyData["type"],
            user=request.user
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
        property = Reminder.objects.filter(user=request.user).get(id=propertyData['id'])
        property.property = Property.objects.filter(user=request.user).get(name=propertyData["property"])
        property.detail = propertyData['detail']
        property.reminder_type = propertyData['type']
        property.user = request.user
        property.save()
        data = {
            'user': "data is updated"
        }
        return JsonResponse(data)


def deletereminder(request):
    id1 = request.GET.get('id', None)
    print(id1, "delete")
    Reminder.objects.filter(user=request.user).get(id=id1).delete()
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
    reminder = Reminder.objects.filter(user=request.user).get(id=pk)
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
    reminder = Reminder.objects.filter(user=request.user).get(id=pk)
    qs = Reminder.objects.filter(user=request.user).get(id=pk)
    context = {
        "object": qs,
    }

    if request.method == "POST":
        reminder.delete()
        return HttpResponse('<script type="text/javascript">window.close()</script>')
    return render(request, "reminders/delete.html", context)
