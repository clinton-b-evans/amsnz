import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from properties.models import Property
from .models import Contact
from .forms import ContactForm


# Create your views here.
def home_view(request):
    return render(request, "contacts/home.html", {})


def addcontact(request):
    if request.method == "POST":
        print(request.body, "property")
        propertyData = json.loads(request.body)
        obj = Contact.objects.create(
            first_name=propertyData["first_name"],
            last_name=propertyData["last_name"],
            company_name=propertyData["company_name"],
            occupation=propertyData["occupation"],
            contact_number=propertyData["contact_number"],
            service_area=propertyData["service_area"],
            website_url=propertyData["website_url"],
            notes=propertyData["notes"],
            user=request.user
            )
        property = Property.objects.filter(name__in=propertyData["properties"])
        obj.properties.update(*property)
        user = {
            'id': obj.id
        }
        data = {
            'user': user
        }
        print(data, 'data')
        return JsonResponse(data)


def editcontact(request):
    if request.method == "POST":
        print(request.body, "property")
        propertyData = json.loads(request.body)
        contact = Contact.objects.get(id=propertyData['id'])
        contact.first_name = propertyData["first_name"]
        contact.last_name = propertyData["last_name"]
        contact.company_name = propertyData["company_name"]
        contact.occupation = propertyData["occupation"]
        contact.contact_number = propertyData["contact_number"]
        contact.service_area = propertyData["service_area"]
        contact.website_url = propertyData["website_url"]
        contact.notes = propertyData["notes"]
        property = Property.objects.filter(name__in=propertyData["properties"])
        contact.properties.add(*property)
        contact.save()
        data = {
            'user': "data is updated"
        }
        return JsonResponse(data)


def deletecontact(request):
    id1 = request.GET.get('id', None)
    print(id1, "delete")
    Contact.objects.get(id=id1).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)


@login_required(login_url='/login/')
def contact_list_view(request):
    property = Property.objects.filter(user=request.user)
    qs = Contact.objects.filter(user=request.user)
    print(qs)
    context = {
        "object_list": qs,
        "property": property
    }
    return render(request, "contacts/main.html", context)


def add_contact(request):
    submitted = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    else:
        form = ContactForm
        if "submitted" in request.GET:
            submitted = True
    form = ContactForm
    return render(request, "contacts/add.html", {"form": form, "submitted": submitted})


def update_contact(request, pk):
    contact = Contact.objects.get(id=pk)
    form = ContactForm(instance=contact)

    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    context = {"form": form}
    return render(request, "contacts/add.html", context)


def delete_contact(request, pk):
    contact = Contact.objects.get(id=pk)
    qs = Contact.objects.get(id=pk)
    context = {
        "object": qs,
    }

    if request.method == "POST":
        # delete object
        contact.delete()
        # after deleting redirect to
        # home page
        return HttpResponse('<script type="text/javascript">window.close()</script>')
    return render(request, "contacts/delete.html", context)
