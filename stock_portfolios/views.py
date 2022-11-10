from django.shortcuts import render
from django.http import HttpResponse
from yahooquery import Ticker

from .models import Stock, StockTransaction
from .forms import StockForm, TransactionForm
import yfinance as yf
from datetime import date, timedelta


def compute_pie_chart_transaction_types(stocks, totalMarketValue, stock_prices):
    pie_chart_data = []
    for stock in stocks:
        percentage = ((float(stock.quantity) * float(stock_prices[stock.ticker])) / totalMarketValue) * 100
        pie_chart_data.append({
            "name": stock.name,
            "percentage": percentage
        })
    return pie_chart_data


def generate_bar_graph_series_data(stocks, stock_prices):
    investments = []
    assetsGains = []
    for stock in stocks:
        spotPrice = stock_prices[stock.ticker]
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


def stock_list_view(request):
    stocks = Stock.objects.exclude(quantity=0)
    used_stocks_ticker = stocks.values_list('ticker', flat=True).distinct()
    stock_prices = get_stock_price_data(used_stocks_ticker)
    investments, assetsGains = generate_bar_graph_series_data(stocks, stock_prices)

    transactions_table = []
    totalInvestment = 0
    totalMarketValue = 0

    for stock in stocks:
        spotPrice = stock_prices[stock.ticker]
        totalInvestment += stock.investment
        currentMarketValue = float(stock.quantity) * spotPrice
        totalMarketValue += currentMarketValue
        status = 'no-gain'
        if (float(currentMarketValue) - float(stock.investment)) > 0:
            status = 'profit'
        elif (float(currentMarketValue) - float(stock.investment)) < 0:
            status = 'loss'
        transactions_table.append({
            "name": stock.name,
            "ticker": stock.ticker,
            "quantity": stock.quantity,
            "totalInvestment": stock.investment,
            "spotPrice": spotPrice,
            "currentMarketValue": currentMarketValue,
            "profit_loss_percentage": ((float(currentMarketValue) - float(stock.investment)) / float(
                stock.investment)) * 100 if stock.investment > 0 else 'N/A',
            "status": status
        })

    context = {
        "transactions": transactions_table,
        "stock_prices": stock_prices,
        "totalInvestment": totalInvestment,
        "totalMarketValue": totalMarketValue,
        "usedStock": stocks.values_list('name', flat=True).distinct(),
        "investments": investments,
        "assetsGains": assetsGains,
        "pie_chart_date": compute_pie_chart_transaction_types(stocks, totalMarketValue, stock_prices)

    }
    return render(request, "stock/main.html", context)


def add_stock(request):
    today = date.today().isoformat()

    submitted = False
    if request.method == "POST":
        ticker_input = request.POST.get("ticker")
        ticker = ticker_input + "-USD"

        yf_data = yf.Ticker(ticker)
        yf_data = yf_data.history(today, interval="60m")
        spot_price = 0.0

        if yf_data["Close"].empty:
            return HttpResponse(
                f"-{ticker_input} No data found, symbol/Ticker may be de-listed!. Kindly try again with correct Ticker."
            )
        else:
            last_price = yf_data["Close"][0]
            string_price = "{:.4f}".format(last_price)
            spot_price += float(string_price)

        form = StockForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.spot_price = spot_price
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
        else:
            form = StockForm
            if "submitted" in request.GET:
                submitted = True
        # else:
        #     messages.error(request, "This Ticker Spot price is not available!")
        #     return redirect("crypto:crypto-add")
    form = StockForm
    return render(request, "stock/add.html", {"form": form, "submitted": submitted})


def stock_transactions(request, year=''):
    if year == '':
        transactions = StockTransaction.objects.all().order_by('date')
    else:
        transactions = StockTransaction.objects.filter(date__year=year).order_by('date')

    transactions_table = []
    for transaction in transactions:
        totalInvestment = float(transaction.quantity) * float(transaction.spot_price)
        transactions_table.append({
            "id": transaction.id,
            "stock_name": transaction.stock,
            "transaction_type": transaction.transaction_type,
            "quantity": transaction.quantity,
            "purchasedValue": transaction.spot_price,
            "date": transaction.date,
            "totalInvestment": totalInvestment,
        })

    context = {
        "year": year,
        "transactions": transactions_table,
    }
    return render(request, "stockTransactions/transactions.html", context)


def add_transaction(request, **kwargs):
    submitted = False
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            if form.data["transaction_type"] == 'Buy':
                form.instance.stock.quantity += float(form.data["quantity"])
                form.instance.stock.investment += float(form.data["quantity"]) * float(form.data["spot_price"])
                form.instance.stock.save()
            else:
                form.instance.stock.quantity -= float(form.data["quantity"])
                if form.instance.stock.investment - float(form.data["quantity"]) * float(form.data["spot_price"]) < 0:
                    form.instance.stock.investment = 0.0
                else:
                    form.instance.stock.investment -= float(form.data["quantity"]) * float(form.data["spot_price"])
                form.instance.stock.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    else:
        form = TransactionForm
        if "submitted" in request.GET:
            submitted = True
    form = TransactionForm
    return render(
        request, "stockTransactions/add.html", {"form": form, "submitted": submitted}
    )


def update_transaction(request, pk):
    transaction = StockTransaction.objects.get(id=pk)
    form = TransactionForm(instance=transaction)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            if form.data["transaction_type"] == 'Buy':
                if form.cleaned_data["spot_price"]:
                    if form.cleaned_data["quantity"]:
                        form.instance.stock.quantity -= float(form.initial["quantity"])
                        form.instance.stock.quantity += float(form.cleaned_data["quantity"])
                        form.instance.stock.investment -= float(form.initial["quantity"]) * float(
                            form.initial["spot_price"])
                        form.instance.stock.investment += float(form.cleaned_data["quantity"]) * float(
                            form.cleaned_data["spot_price"])
                        form.instance.stock.save()
                    else:
                        form.instance.stock.investment -= float(form.initial["quantity"]) * float(
                            form.initial["spot_price"])
                        form.instance.stock.investment += float(form.initial["quantity"]) * float(
                            form.cleaned_data["spot_price"])
                        form.instance.stock.save()

                if form.cleaned_data["quantity"] and not form.cleaned_data["spot_price"]:
                    form.instance.stock.quantity -= float(form.initial["quantity"])
                    form.instance.stock.quantity += float(form.cleaned_data["quantity"])
                    form.instance.stock.investment -= float(form.initial["quantity"]) * float(
                        form.initial["spot_price"])
                    form.instance.stock.investment += float(form.cleaned_data["quantity"]) * float(
                        form.initial["spot_price"])
                    form.instance.stock.save()
                if form.cleaned_data["date"]:
                    form.instance.stock.date = form.cleaned_data["date"]

            else:
                if form.initial["spot_price"]:
                    if form.cleaned_data["quantity"]:
                        form.instance.stock.quantity -= float(form.initial["quantity"])
                        form.instance.stock.quantity += float(form.cleaned_data["quantity"])
                        form.instance.stock.investment += float(form.initial["quantity"]) * float(
                            form.initial["spot_price"])
                        form.instance.stock.investment -= float(form.cleaned_data["quantity"]) * float(
                            form.cleaned_data["spot_price"])
                    else:
                        form.instance.stock.investment += float(form.initial["quantity"]) * float(
                            form.initial["spot_price"])
                        form.instance.stock.investment -= float(form.initial["quantity"]) * float(
                            form.cleaned_data["spot_price"])

                    form.instance.stock.save()

                if form.cleaned_data["quantity"] and not form.cleaned_data["spot_price"]:
                    form.instance.stock.quantity -= float(form.initial["quantity"])
                    form.instance.stock.quantity += float(form.cleaned_data["quantity"])
                    form.instance.stock.investment += float(form.initial["quantity"]) * float(
                        form.initial["spot_price"])
                    form.instance.stock.investment -= float(form.cleaned_data["quantity"]) * float(
                        form.initial["spot_price"])
                    form.instance.stock.save()
                if form.cleaned_data["date"]:
                    form.instance.stock.date = form.cleaned_data["date"]
        form.save()
        return HttpResponse(
            '<script type="text/javascript">window.close()</script>'
        )
    context = {"form": form}
    return render(request, "stockTransactions/add.html", context)




def delete_transaction(request, pk):
    transaction = StockTransaction.objects.get(id=pk)
    qs = StockTransaction.objects.get(id=pk)
    context = {
        "object": qs,
    }

    if request.method == "POST":
        # delete object
        if transaction.transaction_type == 'Buy':
            transaction.stock.quantity -= float(transaction.quantity)
            transaction.stock.investment -= float(transaction.quantity) * float(transaction.spot_price)
            transaction.stock.save()
        else:
            transaction.stock.quantity += float(transaction.quantity)
            transaction.stock.investment += float(transaction.quantity) * float(transaction.spot_price)
            transaction.stock.save()
        transaction.delete()
        # after deleting redirect to
        # home page
        return HttpResponse('<script type="text/javascript">window.close()</script>')

    return render(request, "stockTransactions/delete.html", context)
