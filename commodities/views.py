from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Commodity, Transaction
from .forms import CommodityForm, TransactionForm

def commodity_list_view(request):
    qs = Commodity.objects.all()
    invested_total = 0
    for item in qs:
        item.totalweight = 0
        item.invested = 0
        qs2 = Transaction.objects.filter(commodity=item.pk)
        for items in qs2:
            if items.transaction_type == "Buy":
                item.totalweight += items.weight
                item.invested += items.value
            if items.transaction_type == "Sell":
                item.totalweight -= items.weight
                item.invested -= items.value
        item.total = item.totalweight * item.spot_price
        invested_total += item.invested
    grand_total = 0

    for item in qs:
        grand_total += item.total

    for item in qs:
        item.percent = (item.total / grand_total) * 100

    context = {
        "object_list": qs,
        "grand_total": grand_total,
        "invested_total": invested_total,
    }
    return render(request, "commodities/main.html", context)


def commodity_detail_view(request, **kwargs):
    pk = kwargs.get("pk")
    obj = Commodity.objects.get(pk=pk)
    transactions = Transaction.objects.filter(commodity=obj)
    name = obj.commodity_class

    context = {
        "transactions": transactions,
        "name": name,
        "commodity": pk,
    }
    return render(request, "commodities/detail.html", context)


def add_commodity(request):
    submitted = False
    if request.method == "POST":
        form = CommodityForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    else:
        form = CommodityForm
        if "submitted" in request.GET:
            submitted = True
    form = CommodityForm
    return render(
        request, "commodities/add.html", {"form": form, "submitted": submitted}
    )


def update_commodity(request, pk):
    commodity = Commodity.objects.get(id=pk)
    form = CommodityForm(instance=commodity)

    if request.method == "POST":
        form = CommodityForm(request.POST, instance=commodity)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    context = {"form": form}
    return render(request, "commodities/add.html", context)


def delete_commodity(request, pk):
    commodity = Commodity.objects.get(id=pk)
    qs = Commodity.objects.get(id=pk)
    context = {
        "object": qs,
    }

    if request.method == "POST":
        # delete object
        commodity.delete()
        # after deleting redirect to
        # home page
        return HttpResponse('<script type="text/javascript">window.close()</script>')

    return render(request, "commodities/delete.html", context)


def add_transaction(request, **kwargs):
    submitted = False
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    else:
        form = TransactionForm
        if "submitted" in request.GET:
            submitted = True
    form = TransactionForm
    return render(
        request, "transactions/add.html", {"form": form, "submitted": submitted}
    )


def update_transaction(request, pk):
    transaction = Transaction.objects.get(id=pk)
    form = TransactionForm(instance=transaction)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    context = {"form": form}
    return render(request, "transactions/add.html", context)


def delete_transaction(request, pk):
    transaction = Transaction.objects.get(id=pk)
    qs = Transaction.objects.get(id=pk)
    context = {
        "object": qs,
    }

    if request.method == "POST":
        # delete object
        transaction.delete()
        # after deleting redirect to
        # home page
        return HttpResponse('<script type="text/javascript">window.close()</script>')

    return render(request, "transactions/delete.html", context)
