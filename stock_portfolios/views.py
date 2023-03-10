import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from yahooquery import Ticker

from incomestatements_property.views import sort_years_list
from .models import Stock, StockTransaction
from .forms import StockForm, TransactionForm, StockTickerForm
import yfinance as yf
from datetime import date, timedelta


def compute_pie_chart_transaction_types(stocks, totalMarketValue, stock_prices):
    pie_chart_data = []
    for stock in stocks:
        percentage = ((float(stock.quantity) * float(stock_prices[stock.stock_ticker.ticker])) / totalMarketValue) * 100
        pie_chart_data.append({
            "name": stock.stock_ticker.name,
            "percentage": percentage
        })
    return pie_chart_data


def generate_bar_graph_series_data(stocks, stock_prices):
    investments = []
    assetsGains = []
    for stock in stocks:
        spotPrice = stock_prices[stock.stock_ticker.ticker]
        currentMarketValue = float(stock.quantity) * spotPrice
        assetsGains.append(
            0 if float(currentMarketValue) < float(stock.investment) else float(currentMarketValue) - float(
                stock.investment))
        investments.append(float(stock.investment))

    return investments, assetsGains


def get_stock_price_data(tickers):
    all_symbols = " ".join(tickers)
    myInfo = Ticker(all_symbols)
    data = myInfo.price
    result = dict.fromkeys(data.keys())
    for key, value in data.items():
        result[key] = value['regularMarketPrice']
    return result


@login_required(login_url='/login/')
def stock_list_view(request, year):
    stocks = Stock.objects.filter(user=request.user).exclude(quantity=0)
    used_stocks_ticker = stocks.values_list('stock_ticker__ticker', flat=True).distinct()
    stock_prices = get_stock_price_data(used_stocks_ticker)
    investments, assetsGains = generate_bar_graph_series_data(stocks, stock_prices)

    transactions_table = []
    totalInvestment = 0
    totalMarketValue = 0

    for stock in stocks:
        spotPrice = stock_prices[stock.stock_ticker.ticker]
        totalInvestment += stock.investment
        currentMarketValue = float(stock.quantity) * spotPrice
        totalMarketValue += currentMarketValue
        status = 'no-gain'
        if (float(currentMarketValue) - float(stock.investment)) > 0:
            status = 'profit'
        elif (float(currentMarketValue) - float(stock.investment)) < 0:
            status = 'loss'
        transactions_table.append({
            "name": stock.stock_ticker.name,
            "ticker": stock.stock_ticker.ticker,
            "quantity": stock.quantity,
            "totalInvestment": stock.investment,
            "spotPrice": spotPrice,
            "currentMarketValue": currentMarketValue,
            "profit_loss_percentage": ((float(currentMarketValue) - float(stock.investment)) / float(
                stock.investment)) * 100 if stock.investment > 0 else 'N/A',
            "status": status
        })
    my_investments_list = ['%.2f' % elem for elem in investments]
    my_assetsGains_list = ['%.2f' % elem for elem in assetsGains]
    years = StockTransaction.objects.values_list("date__year").distinct()
    years_list = []
    for data in years:
        for item in data:
            years_list.append(item)
    years_list = sort_years_list(years_list)
    context = {
        "transactions": transactions_table,
        "stock_prices": stock_prices,
        "totalInvestment": totalInvestment,
        "totalMarketValue": totalMarketValue,
        "usedStock": list(stocks.values_list('stock_ticker__name', flat=True).distinct()),
        "investments": list(map(float, my_investments_list)),
        "assetsGains": list(map(float, my_assetsGains_list)),
        "pie_chart_date": compute_pie_chart_transaction_types(stocks, totalMarketValue, stock_prices),
        "years_list": years_list
    }
    return render(request, "stock/main.html", context)


def add_stock(request):
    if request.method == "POST":
        form = StockTickerForm(request.user, request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.user = request.user
            stock.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "transactionListChanged": None,
                        "showMessage": f"{stock.name} added."
                    })
                })
    else:
        form = StockTickerForm(request.user)
    return render(request, "stock/add.html", {"form": form})


def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.user, request.POST)
        if form.is_valid():
            stock_transaction = form.save(commit=False)
            stock_transaction.user = request.user
            stock_transaction.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "transactionListChanged": None,
                        "showMessage": f"Transaction for {stock_transaction.stock_ticker} is added."
                    })
                })
    else:
        form = TransactionForm(request.user)
    return render(request, "stockTransactions/add.html", {"form": form})


def edit_sufi_transaction(request, pk):
    stock_transaction = get_object_or_404(StockTransaction, pk=pk)
    if request.method == "POST":
        form = TransactionForm(request.user, request.POST, instance=stock_transaction)
        if form.is_valid():
            stock_transaction = form.save(commit=False)
            stock_transaction.user = request.user
            stock_transaction.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "transactionListChanged": None,
                        "showMessage": f"{stock_transaction.stock_ticker} updated."
                    })
                }
            )
    else:
        form = TransactionForm(request.user, instance=stock_transaction)
    return render(request, 'stockTransactions/add.html', {
        'form': form,
        'stock_transactions': stock_transactions,
    })


@login_required(login_url='/login/')
def stock_transactions(request, year):
    if year == '':
        stock = Stock.objects.filter(user=request.user).values()
        transactions = StockTransaction.objects.filter(user=request.user).order_by('date')
    else:
        stock = Stock.objects.filter(user=request.user).values()
        transactions = StockTransaction.objects.filter(user=request.user).order_by('date')

    transactions_table = []
    for transaction in transactions:
        totalInvestment = float(transaction.quantity) * float(transaction.spot_price)
        transactions_table.append({
            "id": transaction.id,
            "stock_name": transaction.stock_ticker,
            "transaction_type": transaction.transaction_type,
            "quantity": transaction.quantity,
            "purchasedValue": transaction.spot_price,
            "date": transaction.date,
            "totalInvestment": totalInvestment,
        })
    years = StockTransaction.objects.values_list("date__year").distinct()
    years_list = []
    for data in years:
        for item in data:
            years_list.append(item)
    years_list = sort_years_list(years_list)
    print(years_list, 'years_list')
    context = {
        "year": year,
        "transactions": transactions_table,
        "stock": stock,
        "years_list": years_list,
    }
    return render(request, "stockTransactions/transactions.html", context)


def transaction_list(request, year=''):
    print(year, "year")
    if year == '':
        stock = Stock.objects.filter(user=request.user).values()
        transactions = StockTransaction.objects.filter(user=request.user).order_by('-date')
    else:
        stock = Stock.objects.filter(user=request.user).values()
        transactions = StockTransaction.objects.filter(user=request.user).order_by('-date')

    transactions_table = []
    for transaction in transactions:
        totalInvestment = float(transaction.quantity) * float(transaction.spot_price)
        transactions_table.append({
            "id": transaction.id,
            "stock_name": transaction.stock_ticker,
            "transaction_type": transaction.transaction_type,
            "quantity": transaction.quantity,
            "purchasedValue": transaction.spot_price,
            "date": transaction.date,
            "totalInvestment": totalInvestment,
        })
    years = StockTransaction.objects.values_list("date__year").distinct()
    years_list = []
    for data in years:
        for item in data:
            years_list.append(item)
    years_list = sort_years_list(years_list)
    # print(years_list, 'years_list')
    context = {
        "year": year,
        "transactions": transactions_table,
        "stock": stock,
        "years_list": years_list,
    }
    return render(request, 'stockTransactions/transaction_list.html', context=context)


def edit_transaction(request):
    if request.method == "POST":
        # getting body data from request
        data = json.loads(request.body)
        # setting the id
        pk = data['transactionId']
        # getting models
        transaction = StockTransaction.objects.get(id=pk, user=request.user)
        stock = Stock.objects.get(name=data['stock'], user=request.user)
        # setting values to variables
        spot_price = data['spot_price']
        quantity = data['quantity']
        # saving data to crypto model
        # when transactions_type is buy
        if transaction.transaction_type == 'Buy':
            # if spot_price changed
            if data["spot_price"] != transaction.spot_price:
                # if quantity changed
                if data["quantity"] != transaction.quantity:
                    stock.quantity -= float(transaction.quantity)
                    stock.quantity += float(data["quantity"])
                    stock.investment -= float(transaction.quantity) * float(
                        transaction.spot_price)
                    stock.investment += float(data["quantity"]) * float(
                        data["spot_price"])
                    stock.save()
                else:
                    stock.investment -= float(transaction.quantity) * float(
                        transaction.spot_price)
                    stock.investment += float(transaction.quantity) * float(
                        data["spot_price"])
                    stock.save()
            # if quantity changed and spotPrice didn't change
            if data["quantity"] != transaction.quantity and data["spot_price"] == transaction.spot_price:
                stock.quantity -= float(transaction.quantity)
                stock.quantity += float(data["quantity"])
                stock.investment -= float(transaction.quantity) * float(
                    transaction.spot_price)
                stock.investment += float(data["quantity"]) * float(
                    transaction.spot_price)
                stock.save()
        # when transactions_type is sell
        else:
            # if spot_price changed
            if data["spot_price"] != transaction.spot_price:
                # if quantity changed
                if data["quantity"] != transaction.quantity:
                    stock.quantity -= float(transaction.quantity)
                    stock.quantity += float(data["quantity"])
                    stock.investment += float(transaction.quantity) * float(
                        transaction.spot_price)
                    stock.investment -= float(data["quantity"]) * float(
                        data["spot_price"])
                else:
                    stock.investment += float(transaction.quantity) * float(
                        transaction.spot_price)
                    stock.investment -= float(transaction.quantity) * float(
                        data["spot_price"])
                stock.save()
            # if quantity changed and spotPrice didn't change
            if data["quantity"] != transaction.quantity and data["spot_price"] == transaction.spot_price:
                stock.quantity -= float(transaction.quantity)
                stock.quantity += float(data["quantity"])
                stock.investment += float(transaction.quantity) * float(
                    transaction.spot_price)
                stock.investment -= float(data["quantity"]) * float(
                    transaction.spot_price)
                stock.save()
        # saving data to transaction model
        transaction.spot_price = spot_price
        transaction.quantity = quantity
        transaction.save()

        user = {'id': transaction.id, 'transaction_type': transaction.transaction_type,
                'quantity': transaction.quantity,
                'spot_price': transaction.spot_price}

        data = {
            'user': user
        }
        return JsonResponse(data)


def delete_transaction(request):
    id1 = request.GET.get('id', None)
    transaction = StockTransaction.objects.get(id=id1, user=request.user)
    stock = Stock.objects.get(stock_ticker=transaction.stock_ticker,user=request.user)
    if transaction.transaction_type == 'Buy':
        stock.quantity -= transaction.quantity
        stock.investment -= float(transaction.quantity) * float(transaction.spot_price)
        stock.save()
        print('buy')
    else:
        stock.quantity += transaction.quantity
        stock.investment += float(transaction.quantity) * float(transaction.spot_price)
        stock.save()
        print('sell')
    StockTransaction.objects.get(id=id1, user=request.user).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)
