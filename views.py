from django.shortcuts import render
from .models import PersonalBalance
from .forms import PersonalBalanceForm
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def personal_balance_list_view(request):
    qs_asset = PersonalBalance.objects.filter(entry_type="Asset")
    qs_lib = PersonalBalance.objects.filter(entry_type="Liability")
    qs_save = PersonalBalance.objects.filter(entry_type="Savings")
    qs_retirement = PersonalBalance.objects.filter(entry_type="Retirement Acc")
    total_asset = 0
    total_liability = 0
    total_savings = 0
    total_retirement_acc = 0

    for item in qs_asset:
        total_asset = total_asset + item.amount

    for item in qs_lib:
        total_liability = total_liability + item.amount

    for item in qs_save:
        total_savings = total_savings + item.amount

    for item in qs_retirement:
        total_retirement_acc = total_retirement_acc + item.amount
               
    networth = total_asset + total_savings + total_retirement_acc - total_liability
    if networth > 0:
        networth_class = "black"
    else:
        networth_class = "red"
    context = {
        'assets':qs_asset,
        'liability':qs_lib,
        'savings':qs_save,
        'retirement_acc': qs_retirement,
        'total_asset':total_asset,
        'total_liability':total_liability,
        'total_retirement_acc':total_retirement_acc,
        'total_savings':total_savings,
        'networth':networth,
        'networth_class':networth_class,
        }
    return render(request, 'personal_balances/main.html', context)


def add_personal_balance(request):
    submitted = False
    if request.method == "POST":
        form = PersonalBalanceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('<script type="text/javascript">window.close()</script>')
    else:
        form = PersonalBalanceForm
        if 'submitted' in request.GET:
            submitted = True
    form = PersonalBalanceForm
    return render(request, 'personal_balances/add.html', {'form':form, 'submitted':submitted})


def update_personal_balance(request, pk):
    personal_balance = PersonalBalance.objects.get(id=pk)
    form = PersonalBalanceForm(instance=personal_balance)

    if request.method == 'POST':
        form = PersonalBalanceForm(request.POST, instance=personal_balance)
        if form.is_valid():
            form.save()
            return HttpResponse('<script type="text/javascript">window.close()</script>')
    context = {'form':form}
    return render(request, 'personal_balances/add.html', context)

def delete_personal_balance(request, pk):
    personal_balance = PersonalBalance.objects.get(id=pk)
    qs = PersonalBalance.objects.get(id=pk)
    context = {
        'object':qs,
    }
 
 
    if request.method =="POST":
        # delete object
        personal_balance.delete()
        # after deleting redirect to
        # home page
        return HttpResponse('<script type="text/javascript">window.close()</script>')
 
    return render(request, "personal_balances/delete.html", context)
