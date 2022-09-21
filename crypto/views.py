from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Crypto
from .forms import CryptoForm



# Create your views here.
def crypto_list_view(request):
    qs = Crypto.objects.all()
    total = 0
    for obj in qs:
        obj.total = round(obj.qty * obj.spot_price,2)
        total = total + obj.total
        grand_total = 0
    
    for item in qs:
        grand_total += item.total
    
    for item in qs:
        item.percent = (item.total / grand_total) * 100
    context = {
        'object_list':qs,
        'total':total,
    }
    return render(request, 'crypto/main.html', context)


def add_crypto(request):
    submitted = False
    if request.method == "POST":
        form = CryptoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('<script type="text/javascript">window.close()</script>')
    else:
        form = CryptoForm
        if 'submitted' in request.GET:
            submitted = True
    form = CryptoForm
    return render(request, 'crypto/add.html', {'form':form, 'submitted':submitted})

def update_crypto(request, pk):
    crypto = Crypto.objects.get(id=pk)
    form = CryptoForm(instance=crypto)

    if request.method == 'POST':
        form = CryptoForm(request.POST, instance=crypto)
        if form.is_valid():
            form.save()
            return HttpResponse('<script type="text/javascript">window.close()</script>')
    context = {'form':form}
    return render(request, 'crypto/add.html', context)

def delete_crypto(request, pk):
    crypto = Crypto.objects.get(id=pk)
    qs = Crypto.objects.get(id=pk)
    context = {
        'object':qs,
    }
 
    if request.method =="POST":
        # delete object
        crypto.delete()
        # after deleting redirect to
        # home page
        return HttpResponse('<script type="text/javascript">window.close()</script>')
 
    return render(request, "crypto/delete.html", context)
