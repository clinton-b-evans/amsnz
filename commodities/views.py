import json
from decimal import Decimal

import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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


def compute_pie_chart_transaction_types(commodities, totalMarketValue, commodity_prices):
    pie_chart_data = []
    for commodity in commodities:
        percentage = ((float(commodity.weight) * float(
            commodity_prices[commodity.commodity_class])) / totalMarketValue) * 100
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
        assetsGains.append(
            0 if float(currentMarketValue) < float(commodity.investment) else float(currentMarketValue) - float(
                commodity.investment))
        investments.append(float(commodity.investment))

    return investments, assetsGains


@login_required(login_url='/login/')
def commodity_list_view(request, year=""):
    commodities = Commodity.objects.filter(user=request.user).exclude(quantity=0)
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
        if (float(currentMarketValue) - float(commodity.investment)) > 0:
            status = 'profit'
        elif (float(currentMarketValue) - float(commodity.investment)) < 0:
            status = 'loss'
        transactions_table.append({
            "commodity": commodity,
            "weight": commodity.weight,
            "totalInvestment": commodity.investment,
            "spotPrice": spotPrice,
            "currentMarketValue": currentMarketValue,
            "profit_loss_percentage": ((float(currentMarketValue) - float(commodity.investment)) / float(
                commodity.investment)) * 100 if commodity.investment > 0 else 'N/A',
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
        "pie_chart_date": compute_pie_chart_transaction_types(commodities, totalMarketValue, commodity_prices)

    }
    return render(request, "commodities/main.html", context)


@login_required(login_url='/login/')
def commodity_transactions(request, year=''):
    if year == '':
        commodity = Commodity.objects.filter(user=request.user).values()
    else:
        commodity = Commodity.objects.filter(user=request.user, year=year).values()
    if year == '':
        transactions = Transaction.objects.filter(user=request.user).order_by('date')
    else:
        transactions = Transaction.objects.filter(date__year=year, user=request.user).order_by('date')

    transactions_table = []
    for transaction in transactions:
        totalInvestment = float(transaction.weight) * float(transaction.value)
        transactions_table.append({
            "id": transaction.id,
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
        "commodity": commodity,
    }
    return render(request, "commodities/commodity_classes.html", context)


def addTransaction(request):
    if request.method == "POST":
        # getting body data from request
        transactionData = json.loads(request.body)
        # getting models
        commodity = Commodity.objects.get(name=transactionData['commodity'], user=request.user)
        # saving data to crypto model
        # when transactions_type is buy
        if transactionData["transaction_type"] == 'Buy':
            commodity.weight += float(transactionData["weight"])
            commodity.investment += float(transactionData["weight"]) * float(transactionData["value"])
            commodity.save()
        # when transactions_type is sell
        else:
            if commodity.weight - float(transactionData["weight"]) > -1:
                commodity.weight -= float(transactionData["weight"])
                if commodity.investment - float(transactionData["weight"]) * float(transactionData["spot_price"]) < 0:
                    commodity.investment = float(0.0)
                else:
                    commodity.investment -= float(transactionData["weight"]) * float(transactionData["spot_price"])
                commodity.save()
            else:
                data = {
                    "weight": "error"
                }
                return JsonResponse(data)
        obj = Transaction.objects.create(
            commodity=Commodity.objects.get(name=transactionData["commodity"], user=request.user),
            transaction_type=transactionData['transaction_type'],
            weight=transactionData['weight'],
            value=transactionData['value'],
            date=transactionData['date'],
            user=request.user
        )
        user = {
            'id': obj.id,
            'commodity': transactionData['commodity'],
            'value': obj.value,
            'transaction_type': obj.transaction_type,
            'weight': obj.weight,
            'date': obj.date
        }
        data = {
            'user': user
        }
        print(data, 'data')
        return JsonResponse(data)


def edit_transaction(request):
    if request.method == "POST":
        # getting body data from request
        data = json.loads(request.body)
        # setting the id
        pk = data['transactionId']
        # getting models
        transaction = Transaction.objects.get(id=pk, user=request.user)
        commodity = Commodity.objects.get(name=data['commodity'], user=request.user)
        print(commodity.investment, 'crypto')
        # setting values to variables
        value = data['value']
        weight = data['weight']
        # saving data to crypto model
        # when transactions_type is buy
        if transaction.transaction_type == 'Buy':
            # if spot_price changed
            if data["value"] != transaction.value:
                # if quantity changed
                if data["weight"] != transaction.weight:
                    commodity.weight -= float(transaction.weight)
                    commodity.weight += float(data["weight"])
                    commodity.investment -= float(transaction.weight) * float(
                        transaction.value)
                    commodity.investment += float(data["weight"]) * float(
                        data["value"])
                    commodity.save()
                else:
                    commodity.investment -= float(transaction.weight) * float(
                        transaction.value)
                    commodity.investment += float(transaction.weight) * float(
                        data["value"])
                    commodity.save()
            # if quantity changed and spotPrice didn't change
            if data["weight"] != transaction.weight and data["value"] == transaction.value:
                commodity.weight -= float(transaction.weight)
                commodity.weight += float(data["weight"])
                commodity.investment -= float(transaction.weight) * float(
                    transaction.value)
                commodity.investment += float(data["weight"]) * float(
                    transaction.value)
                commodity.save()
        # when transactions_type is sell
        else:
            # if spot_price changed
            if data["value"] != transaction.value:
                # if quantity changed
                if data["weight"] != transaction.weight:
                    commodity.weight -= float(transaction.weight)
                    commodity.weight += float(data["weight"])
                    commodity.investment += float(transaction.weight) * float(
                        transaction.value)
                    commodity.investment -= float(data["weight"]) * float(
                        data["value"])
                else:
                    commodity.investment += float(transaction.weight) * float(
                        transaction.value)
                    commodity.investment -= float(transaction.weight) * float(
                        data["value"])
                commodity.save()
            # if quantity changed and spotPrice didn't change
            if data["weight"] != transaction.weight and data["value"] == transaction.value:
                commodity.weight -= float(transaction.weight)
                commodity.weight += float(data["weight"])
                commodity.weight += float(transaction.weight) * float(
                    transaction.value)
                commodity.investment -= float(data["weight"]) * float(
                    transaction.value)
                commodity.save()
        # saving data to transaction model
        transaction.value = value
        transaction.weight = weight
        transaction.save()

        user = {'id': transaction.id, 'transaction_type': transaction.transaction_type,
                'weight': transaction.weight,
                'value': transaction.value}

        data = {
            'user': user
        }
        return JsonResponse(data)


def commodity_detail_view(request, **kwargs):
    pk = kwargs.get("pk")
    obj = Commodity.objects.get(pk=int(pk), user=request.user)
    transactions = Transaction.objects.filter(commodity=obj, user=request.user)
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
    commodity = Commodity.objects.get(id=pk, user=request.user)
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
    commodity = Commodity.objects.filter(id=pk, user=request.user)
    qs = Commodity.objects.get(id=pk, user=request.user)
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
                form.instance.commodity.weight += float(form.data["weight"])
                form.instance.commodity.investment += float(form.data["weight"]) * float(form.data["value"])
                form.instance.commodity.save()
            else:
                form.instance.commodity.weight -= float(form.data["weight"])
                if form.instance.commodity.investment - float(form.data["weight"]) * float(form.data["value"]) < 0:
                    form.instance.commodity.investment = float(0.0)
                else:
                    form.instance.commodity.investment -= float(form.data["weight"]) * float(form.data["value"])
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
    transaction = Transaction.objects.get(id=pk, user=request.user)
    form = TransactionForm(instance=transaction)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            if form.data["transaction_type"] == 'Buy':
                if form.cleaned_data["value"]:
                    if form.cleaned_data["weight"]:
                        form.instance.commodity.weight -= float(form.initial["weight"])
                        form.instance.commodity.weight += float(form.cleaned_data["weight"])
                        form.instance.commodity.investment -= float(form.initial["weight"]) * float(
                            form.initial["value"])
                        form.instance.commodity.investment += float(form.cleaned_data["weight"]) * float(
                            form.cleaned_data["value"])
                        form.instance.commodity.save()
                    else:
                        form.instance.commodity.investment -= float(form.initial["weight"]) * float(
                            form.initial["value"])
                        form.instance.commodity.investment += float(form.initial["weight"]) * float(
                            form.cleaned_data["value"])
                        form.instance.commodity.save()

                if form.cleaned_data["weight"] and not form.cleaned_data["value"]:
                    form.instance.commodity.weight -= float(form.initial["weight"])
                    form.instance.commodity.weight += float(form.cleaned_data["weight"])
                    form.instance.commodity.investment -= float(form.initial["weight"]) * float(form.initial["value"])
                    form.instance.commodity.investment += float(form.cleaned_data["weight"]) * float(
                        form.initial["value"])
                    form.instance.commodity.save()
                if form.cleaned_data["date"]:
                    form.instance.commodity.date = form.cleaned_data["date"]

            else:
                if form.initial["value"]:
                    if form.cleaned_data["weight"]:
                        form.instance.commodity.weight -= float(form.initial["weight"])
                        form.instance.commodity.weight += float(form.cleaned_data["weight"])
                        form.instance.commodity.investment += float(form.initial["weight"]) * float(
                            form.initial["value"])
                        form.instance.commodity.investment -= float(form.cleaned_data["weight"]) * float(
                            form.cleaned_data["value"])
                    else:
                        form.instance.commodity.investment += float(form.initial["weight"]) * float(
                            form.initial["value"])
                        form.instance.commodity.investment -= float(form.initial["weight"]) * float(
                            form.cleaned_data["value"])

                    form.instance.commodity.save()

                if form.cleaned_data["weight"] and not form.cleaned_data["value"]:
                    form.instance.commodity.weight -= float(form.initial["weight"])
                    form.instance.commodity.weight += float(form.cleaned_data["weight"])
                    form.instance.commodity.investment += float(form.initial["weight"]) * float(form.initial["value"])
                    form.instance.commodity.investment -= float(form.cleaned_data["weight"]) * float(
                        form.initial["value"])
                    form.instance.commodity.save()
                if form.cleaned_data["date"]:
                    form.instance.commodity.date = form.cleaned_data["date"]
            form.save()

            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    context = {"form": form}
    return render(request, "transactions/add.html", context)


def deleteTransaction(request):
    id1 = request.GET.get('id', None)
    transaction = Transaction.objects.get(id=id1, user=request.user)
    if transaction.transaction_type == 'Buy':
        transaction.commodity.weight -= transaction.weight
        transaction.commodity.investment -= float(transaction.weight) * float(transaction.value)
        transaction.commodity.save()
        print('buy')
    else:
        transaction.commodity.weight += transaction.weight
        transaction.commodity.investment += float(transaction.weight) * float(transaction.value)
        transaction.commodity.save()
        print('sell')
    Transaction.objects.get(id=id1).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)


def delete_transaction(request, pk):
    transaction = Transaction.objects.get(id=pk, user=request.user)
    qs = Transaction.objects.get(id=pk, user=request.user)
    context = {
        "object": qs,
    }

    if request.method == "POST":
        # delete object
        if transaction.transaction_type == 'Buy':
            transaction.commodity.weight -= transaction.weight
            transaction.commodity.investment -= float(transaction.weight) * float(transaction.value)
            transaction.commodity.save()
        else:
            transaction.commodity.weight += transaction.weight
            transaction.commodity.investment += float(transaction.weight) * float(transaction.value)
            transaction.commodity.save()
        transaction.delete()
        # after deleting redirect to
        # home page
        return HttpResponse('<script type="text/javascript">window.close()</script>')

    return render(request, "transactions/delete.html", context)
