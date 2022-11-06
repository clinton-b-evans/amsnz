from decimal import Decimal

import requests
from django.shortcuts import render
from django.http import HttpResponse
from yahooquery import Ticker
from yfinance import ticker

from .models import Commodity, Transaction
from .forms import CommodityForm, TransactionForm
from datetime import date
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor

COMMODITIES_API_KEY = "rhk8fw6wof9m507vu59ja24d1cxq56340g3nnt7u81zz0njwzujpj11c93p1"


def sort(myList):
    myList.sort()
    return myList


def get_commodities():
    commodities_list = [
        'GC=F',
        'SI=F',
        'PL=F',
        "PA=F"
    ]
    all_symbols = " ".join(commodities_list)
    myInfo = Ticker(all_symbols)
    data = myInfo.price
    result = dict.fromkeys(data.keys())
    for key, value in data.items():
        result[key] = value['regularMarketPrice']
    return result
def compute_pie_chart_transaction_types(commodities, total_invested):
    pie_chart_data = []
    for commodity in commodities:
        percentage = (commodity.investment/total_invested) * 100
        pie_chart_data.append({
            "commodity": commodity.name,
            "percentage": percentage
        })
    return pie_chart_data

def generate_bar_graph_series_data(commodities, commodity_prices):
    investments = []
    assetsGains = []
    for commodity in commodities:
        spotPrice = commodity_prices[commodity.commodity_class]
        currentMarketValue = float(commodity.weight) * spotPrice
        assetsGains.append(0 if float(currentMarketValue) < float(commodity.investment) else float(currentMarketValue) - float(commodity.investment))
        investments.append(float(commodity.investment))

    return investments, assetsGains


def commodity_list_view(request):
    commodities = Commodity.objects.exclude(weight=0)
    commodity_prices = get_commodities()
    investments, assetsGains = generate_bar_graph_series_data(commodities, commodity_prices)

    transactions_table = []
    totalInvestment = 0
    totalMarketValue = 0

    for commodity in commodities:
        spotPrice = commodity_prices[commodity.commodity_class]
        totalInvestment += commodity.investment
        currentMarketValue = float(commodity.weight) * spotPrice
        totalMarketValue += currentMarketValue
        status = 'no-gain'
        if (float(currentMarketValue) - float(commodity.investment)) > 0 :
            status = 'profit'
        elif (float(currentMarketValue) - float(commodity.investment)) < 0:
            status = 'loss'
        transactions_table.append({
            "commodity": commodity,
            "weight": commodity.weight,
            "totalInvestment": commodity.investment,
            "spotPrice": spotPrice,
            "currentMarketValue": currentMarketValue,
            "profit_loss_percentage": ((float(currentMarketValue) - float(commodity.investment)) / float(commodity.investment)) * 100 if commodity.investment > 0 else 'N/A',
            "status": status
        })

    context = {
        "transactions": transactions_table,
        "commodities_list": commodity_prices,
        "totalInvestmentSum": totalInvestment,
        "currentMarketValueSum": totalMarketValue,
        "usedCommodities": commodities.values_list('name', flat=True).distinct(),
        "investments": investments,
        "assetsGains": assetsGains,
        "pie_chart_date": compute_pie_chart_transaction_types(commodities, totalInvestment)

    }
    return render(request, "commodities/main.html", context)


def commodity_transactions(request, year=''):
    if year == '':
        transactions = Transaction.objects.all().order_by('date')
    else:
        transactions = Transaction.objects.filter(date__year=year).order_by('date')

    transactions_table = []
    for transaction in transactions:
        totalInvestment = float(transaction.weight) * float(transaction.value)
        transactions_table.append({
            "commodity": transaction.commodity,
            "transaction_type": transaction.transaction_type,
            "weight": transaction.weight,
            "purchasedValue": transaction.value,
            "date": transaction.date,
            "totalInvestment": totalInvestment,
        })

    context = {
        "year": year,
        "transactions": transactions_table,
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
            if form.data["transaction_type"] == 'Buy':
                form.instance.commodity.weight += Decimal(form.data["weight"])
                form.instance.commodity.investment += Decimal(form.data["weight"]) * Decimal(form.data["value"])
                form.instance.commodity.save()
            else:
                form.instance.commodity.weight -= Decimal(form.data["weight"])
                if form.instance.commodity.investment - Decimal(form.data["weight"]) * Decimal(form.data["value"]) < 0:
                    form.instance.commodity.investment = Decimal(0.0)
                else:
                    form.instance.commodity.investment -= Decimal(form.data["weight"]) * Decimal(form.data["value"])
                form.instance.commodity.save()
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
