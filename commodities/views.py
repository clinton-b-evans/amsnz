import requests
from django.shortcuts import render
from django.http import HttpResponse
from .models import Commodity, Transaction
from .forms import CommodityForm, TransactionForm

COMMODITIES_API_KEY = "rhk8fw6wof9m507vu59ja24d1cxq56340g3nnt7u81zz0njwzujpj11c93p1"


def sort(myList):
    myList.sort()
    return myList


def commodity_list_view(request, year):
    commodities = Commodity.objects.filter(date__year=year)
    transactions_obj = Transaction.objects.filter(date__year=year)
    invested_total = 0
    for commodity in commodities:
        commodity.totalWeight = 0
        commodity.invested = 0
        transactions = Transaction.objects.filter(
            commodity=commodity.pk, date__year=year
        )
        for transaction in transactions:
            commodity.trans_ob = transaction
            if transaction.transaction_type == "Buy":
                commodity.totalWeight += transaction.weight
                commodity.invested += transaction.value
            if transaction.transaction_type == "Sell":
                commodity.totalWeight -= transaction.weight
                commodity.invested -= transaction.value
        commodity.total = commodity.totalWeight * commodity.spot_price
        invested_total += commodity.invested
    grand_total = 0

    for commodity in commodities:
        grand_total += commodity.total

    for commodity in commodities:
        commodity.percentage = (commodity.total / grand_total) * 100
        if commodity.percentage < 0:
            commodity.percentage = 0.0

    years = list(Transaction.objects.values_list("date__year").distinct())
    years_list = []
    for each in years:
        for item in each:
            years_list.append(item)

    years_list = sort(years_list)
    invested_total_year_wise = 0
    commodities_invested_all_years_total_list = []

    for my_year in years_list:
        commodities_list = Commodity.objects.filter(date__year=my_year)
        for item in commodities_list:
            item.totalweight = 0
            item.invested = 0
            transaction_list = Transaction.objects.filter(
                commodity=item.pk, date__year=my_year
            )
            for items in transaction_list:
                if items.transaction_type == "Buy":
                    item.totalweight += items.weight
                    item.invested += items.value
                if items.transaction_type == "Sell":
                    item.totalweight -= items.weight
                    item.invested -= items.value
            item.total = item.totalweight * item.spot_price
            invested_total_year_wise += item.invested
        commodities_invested_all_years_total_list.append(
            float(invested_total_year_wise)
        )

    context = {
        "year": year,
        "object_list": commodities,
        "transactions_obj": transactions_obj,
        "grand_total": grand_total,
        "invested_total": invested_total,
        "commodities_invested_all_years_total_list": commodities_invested_all_years_total_list,
        "years_list": years_list,
        # 'commodity_classes': commodity_classes,
    }
    return render(request, "commodities/main.html", context)


def commodities_latest_price_view(request):
    commodity_classes = Commodity.objects.all()

    for commodity in commodity_classes:
        url = (
            f"https://commodities-api.com/api/latest?access_key={COMMODITIES_API_KEY}"
            f"&base=USD&symbols={commodity.commodity_class}"
        )
        response = requests.request("GET", url)
        result = response.json()
        last_price = 1 / result["data"]["rates"][commodity.commodity_class]
        string_price = "{:.4f}".format(last_price)
        commodity.latest_price = float(string_price)

    context = {
        "commodity_classes": commodity_classes,
    }
    return render(request, "commodities/commodity_classes.html", context)


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
        commodity_class = request.POST.get("commodity_class")
        url = f"https://commodities-api.com/api/latest?access_key=rhk8fw6wof9m507vu59ja24d1cxq56340g3nnt7u81zz0njwzujpj11c93p1&base=USD&symbols={commodity_class}"
        response = requests.request("GET", url)
        result = response.json()
        spot_price = 0
        if result["data"]["success"]:
            last_price = 1 / result["data"]["rates"][commodity_class]
            string_price = "{:.4f}".format(last_price)
            spot_price += float(string_price)
        else:
            return HttpResponse(
                "No ticker data or an invalid value has been specified, Data not found "
            )

        form = CommodityForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.spot_price = spot_price
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
    commodity = Commodity.objects.filter(id=pk)
    qs = Commodity.objects.get(id=pk)
    context = {
        "object": qs,
    }

    if request.method == "POST":
        commodity.delete()
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
