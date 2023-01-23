import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from incomestatements_property.views import sort_years_list
from .models import PersonalBalance
from .forms import PersonalBalanceForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse


@login_required(login_url='/login/')
def personal_balance_list_view(request, year):
    selected = "Yearly"

    qs_asset = PersonalBalance.objects.filter(entry_type="Asset", user=request.user, date__year=year)
    qs_lib = PersonalBalance.objects.filter(entry_type="Liability", user=request.user, date__year=year)
    qs_save = PersonalBalance.objects.filter(entry_type="Savings", user=request.user, date__year=year)
    qs_retirement = PersonalBalance.objects.filter(entry_type="Retirement Acc", user=request.user, date__year=year)
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
    years = PersonalBalance.objects.filter(user=request.user).values_list("date__year").distinct()
    years_list = []
    for data in years:
        for item in data:
            years_list.append(item)
    years_list = sort_years_list(years_list)
    print(years_list, 'years')
    context = {
        "assets": qs_asset,
        "liability": qs_lib,
        "savings": qs_save,
        "retirement_acc": qs_retirement,
        "total_asset": total_asset,
        "total_liability": total_liability,
        "total_retirement_acc": total_retirement_acc,
        "total_savings": total_savings,
        "networth": networth,
        "networth_class": networth_class,
        "selected": selected,
        "years_list": years_list,
    }
    return render(request, "personal_balances/main.html", context)


def personal_balance_list_monthly(request):
    selected = "Monthly"

    qs_asset = PersonalBalance.objects.filter(entry_type="Asset", user=request.user)
    qs_lib = PersonalBalance.objects.filter(entry_type="Liability", user=request.user)
    qs_save = PersonalBalance.objects.filter(entry_type="Savings", user=request.user)
    qs_retirement = PersonalBalance.objects.filter(entry_type="Retirement Acc", user=request.user)

    total_asset = 0
    total_liability = 0
    total_savings = 0
    total_retirement_acc = 0

    for item in qs_asset:
        total_asset = total_asset + item.amount
        total_asset = round(total_asset / 12, 2)

    for item in qs_lib:
        total_liability = total_liability + item.amount
        total_liability = round(total_liability / 12, 2)

    for item in qs_save:
        total_savings = total_savings + item.amount
        total_savings = round(total_savings / 12, 2)

    for item in qs_retirement:
        total_retirement_acc = total_retirement_acc + item.amount
        total_retirement_acc = round(total_retirement_acc / 12, 2)

    networth = total_asset + total_savings + total_retirement_acc - total_liability
    if networth > 0:
        networth_class = "black"
    else:
        networth_class = "red"
    context = {
        "assets": qs_asset,
        "liability": qs_lib,
        "savings": qs_save,
        "retirement_acc": qs_retirement,
        "total_asset": total_asset,
        "total_liability": total_liability,
        "total_retirement_acc": total_retirement_acc,
        "total_savings": total_savings,
        "networth": networth,
        "networth_class": networth_class,
        "selected": selected,
    }
    return render(request, "personal_balances/main.html", context)


def personal_balance_list_weekly(request):
    selected = "Weekly"

    qs_asset = PersonalBalance.objects.filter(entry_type="Asset", user=request.user)
    qs_lib = PersonalBalance.objects.filter(entry_type="Liability", user=request.user)
    qs_save = PersonalBalance.objects.filter(entry_type="Savings", user=request.user)
    qs_retirement = PersonalBalance.objects.filter(entry_type="Retirement Acc", user=request.user)

    total_asset = 0
    total_liability = 0
    total_savings = 0
    total_retirement_acc = 0

    for item in qs_asset:
        total_asset = total_asset + item.amount
        total_asset = round(total_asset / 52, 2)

    for item in qs_lib:
        total_liability = total_liability + item.amount
        total_liability = round(total_liability / 52, 2)

    for item in qs_save:
        total_savings = total_savings + item.amount
        total_savings = round(total_savings / 52, 2)

    for item in qs_retirement:
        total_retirement_acc = total_retirement_acc + item.amount
        total_retirement_acc = round(total_retirement_acc / 52, 2)

    networth = total_asset + total_savings + total_retirement_acc - total_liability
    if networth > 0:
        networth_class = "black"
    else:
        networth_class = "red"
    context = {
        "assets": qs_asset,
        "liability": qs_lib,
        "savings": qs_save,
        "retirement_acc": qs_retirement,
        "total_asset": total_asset,
        "total_liability": total_liability,
        "total_retirement_acc": total_retirement_acc,
        "total_savings": total_savings,
        "networth": networth,
        "networth_class": networth_class,
        "selected": selected,
    }
    return render(request, "personal_balances/main.html", context)


def addpersonal_balance(request):
    if request.method == "POST":
        print(request.body, "property")
        categoryData = json.loads(request.body)
        obj = PersonalBalance.objects.create(
            description=categoryData['description'],
            entry_type=categoryData["entry"],
            amount=categoryData["amount"],
            date=categoryData["date"],
            user=request.user
        )
        user = {
            'name': obj.description,
        }
        data = {
            'user': user
        }
        print(data, 'data')
        return JsonResponse(data)


def updatepersonal_balance(request):
    if request.method == "POST":
        print(request.body, "property")
        propertyData = json.loads(request.body)
        property = PersonalBalance.objects.filter(user=request.user).get(id=propertyData['id'])
        property.description = propertyData['description']
        property.entry_type = propertyData["entry"]
        property.amount = propertyData['amount']
        property.save()
        data = {
            'user': "data is updated"
        }
        return JsonResponse(data)


def deletepersonal_balance(request):
    id1 = request.GET.get('id', None)
    print(id1, "delete")
    PersonalBalance.objects.filter(user=request.user).get(id=id1).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)


def add_personal_balance(request):
    submitted = False
    if request.method == "POST":
        form = PersonalBalanceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    else:
        form = PersonalBalanceForm
        if "submitted" in request.GET:
            submitted = True
    form = PersonalBalanceForm
    return render(
        request, "personal_balances/add.html", {"form": form, "submitted": submitted}
    )


def update_personal_balance(request, pk):
    personal_balance = PersonalBalance.objects.filter(user=request.user).get(id=pk)
    form = PersonalBalanceForm(instance=personal_balance)

    if request.method == "POST":
        form = PersonalBalanceForm(request.POST, instance=personal_balance)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    context = {"form": form}
    return render(request, "personal_balances/add.html", context)


def delete_personal_balance(request, pk):
    personal_balance = PersonalBalance.objects.filter(user=request.user).get(id=pk)
    qs = PersonalBalance.objects.filter(user=request.user).get(id=pk)
    context = {
        "object": qs,
    }

    if request.method == "POST":
        # delete object
        personal_balance.delete()
        # after deleting redirect to
        # home page
        return HttpResponse('<script type="text/javascript">window.close()</script>')
    return render(request, "personal_balances/delete.html", context)
