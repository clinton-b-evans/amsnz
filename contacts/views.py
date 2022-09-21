from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Contact
from .forms import ContactForm


# Create your views here.
def home_view(request):
    return render(request, 'contacts/home.html', {})


def contact_list_view(request):
    qs = Contact.objects.all()
    print(qs)
    context = {
        'object_list':qs,
    }
    return render(request, 'contacts/main.html', context)


def add_contact(request):
    submitted = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('<script type="text/javascript">window.close()</script>')
    else:
        form = ContactForm
        if 'submitted' in request.GET:
            submitted = True
    form = ContactForm
    return render(request, 'contacts/add.html', {'form':form, 'submitted':submitted})


def update_contact(request, pk):
    contact = Contact.objects.get(id=pk)
    form = ContactForm(instance=contact)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return HttpResponse('<script type="text/javascript">window.close()</script>')
    context = {'form':form}
    return render(request, 'contacts/add.html', context)

def delete_contact(request, pk):
    contact = Contact.objects.get(id=pk)
    qs = Contact.objects.get(id=pk)
    context = {
        'object':qs,
    }
 
 
    if request.method =="POST":
        # delete object
        contact.delete()
        # after deleting redirect to
        # home page
        return HttpResponse('<script type="text/javascript">window.close()</script>')
 
    return render(request, "contacts/delete.html", context)
