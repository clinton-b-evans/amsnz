from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from properties.models import Property
from reminders.models import Reminder
from django.db.models import Sum
from datetime import date
from .forms import ReminderForm

# Create your views here.

def home_view(request):
    return render(request, 'reminders/home.html', {})

def reminder_list_view(request):
    qs = Reminder.objects.all().order_by('due_date')
    context = {
        'object_list':qs,
    }
    return render(request, 'reminders/main.html', context)
    
def add_reminder(request):
    submitted = False
    if request.method == "POST":
        form = ReminderForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('<script type="text/javascript">window.close()</script>')
    else:
        form = ReminderForm
        if 'submitted' in request.GET:
            submitted = True
    form = ReminderForm
    return render(request, 'reminders/add_reminders.html', {'form':form, 'submitted':submitted})

def update_reminder(request, pk):
    reminder = Reminder.objects.get(id=pk)
    form = ReminderForm(instance=reminder)

    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            return HttpResponse('<script type="text/javascript">window.close()</script>')
    context = {'form':form}
    return render(request, 'reminders/add_reminders.html', context)

def delete_reminder(request, pk):
    reminder = Reminder.objects.get(id=pk)
    qs = Reminder.objects.get(id=pk)
    context = {
        'object':qs,
    }
 
    if request.method =="POST":
        # delete object
        reminder.delete()
        # after deleting redirect to
        # home page
        return HttpResponse('<script type="text/javascript">window.close()</script>')
 
    return render(request, "reminders/delete.html", context)
