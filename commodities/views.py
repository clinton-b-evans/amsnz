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
        'ROKU',
        'QCOM',
        'GOLD',
        'HOOD',
        'ETSY',
        'SU',
        'LUMN',
        'REGN',
        'CI',
        'MAR',
        'APD',
        'SQQQ',
        'FTNT',
        'BKNG',
        'EBAY',
        'MRNA',
        'RUN',
        'GBPUSD=X',
        'NQ=F',
        'COMS',
        'NFLX',
        'HUBS',
        'EURUSD=X',
        'ARKK',
        'MATIC-USD',
        'DDOG',
        'SPY',
        'NETC.CO',
        'TQQQ',
        'BT-A.L',
    ]
    all_symbols = " ".join(commodities_list)
    myInfo = Ticker(all_symbols)
    data = myInfo.price
    result = dict.fromkeys(data.keys())
    for key, value in data.items():
        result[key] = value['regularMarketPrice']
    return result
def compute_pie_chart_transaction_types(transactions, total):
    commodities = transactions.values_list("commodity").distinct()
    pie_chart_data = []
    for commodity in commodities:
        commodity_transactions = transactions.filter(commodity=commodity[0])
        invested = 0
        for commodity_transaction in commodity_transactions:
            invested += float(commodity_transaction.value) * float(commodity_transaction.weight)
        percentage = (invested/total)*100
        pie_chart_data.append({
            "commodity": commodity[0],
            "percentage": percentage
        })
    return pie_chart_data

def commodity_list_view(request, year):
    transactions = Transaction.objects.filter(date__year=year, transaction_type='Buy')
    years = list(Transaction.objects.values_list("date__year").distinct())
    years_list = []
    for each in years:
        for item in each:
            years_list.append(item)
    commodity_prices = get_commodities()
    years_list = sort(years_list)
    purchased_data = []
    selling_data = []
    for curr_year in years_list:
        bought = 0
        sell = 0
        yearly_transactions = Transaction.objects.filter(date__year=curr_year)
        for curr_transaction in yearly_transactions:
            if curr_transaction.transaction_type == 'Buy':
                bought += curr_transaction.weight * curr_transaction.value
            else:
                sell += curr_transaction.weight * curr_transaction.value
        purchased_data.append(float(bought))
        selling_data.append(float(sell))
    transactions_table = []
    totalInvestmentSum = 0
    currentMarketValueSum = 0
    for transaction in transactions:
        totalInvestment = float(transaction.weight) * float(transaction.value)
        totalInvestmentSum += totalInvestment
        spotPrice = commodity_prices[transaction.commodity]
        currentMarketValue = float(transaction.weight) * spotPrice
        currentMarketValueSum += currentMarketValue
        status = 'no-gain'
        if (currentMarketValue - totalInvestment) > 0 :
            status = 'profit'
        elif (currentMarketValue - totalInvestment) < 0:
            status = 'loss'
        transactions_table.append({
            "commodity": transaction.commodity,
            "transaction_type": transaction.transaction_type,
            "weight": transaction.weight,
            "purchasedValue": transaction.value,
            "date": transaction.date,
            "totalInvestment": totalInvestment,
            "spotPrice": spotPrice,
            "currentMarketValue": currentMarketValue,
            "profit_loss_percentage": ((currentMarketValue - totalInvestment) / totalInvestment) * 100,
            "status": status
        })

    context = {
        "year": year,
        "years_list": years_list,
        "transactions": transactions_table,
        "commodities_list": commodity_prices,
        "totalInvestmentSum": totalInvestmentSum,
        "currentMarketValueSum": currentMarketValueSum,
        "purchased_data": purchased_data,
        "sold_data": selling_data,
        "pie_chart_date": compute_pie_chart_transaction_types(transactions, totalInvestmentSum)

    }
    return render(request, "commodities/main.html", context)


def commodity_transactions(request, year):
    transactions = Transaction.objects.filter(date__year=year)

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
