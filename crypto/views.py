from decimal import Decimal

from django.shortcuts import render
from django.http import HttpResponse
from yahooquery import Ticker

from .models import Crypto, CryptoTransaction
from .forms import CryptoForm, TransactionForm
import yfinance as yf
from datetime import date, timedelta
def compute_pie_chart_transaction_types(cryptos, totalMarketValue, crypto_prices):
    pie_chart_data = []
    for crypto in cryptos:
        percentage = ((float(crypto.quantity) * float(crypto_prices[crypto.ticker]))/totalMarketValue) * 100
        pie_chart_data.append({
            "name": crypto.name,
            "percentage": percentage
        })
    return pie_chart_data

def generate_bar_graph_series_data(cryptos, crypto_prices):
    investments = []
    assetsGains = []
    for crypto in cryptos:
        spotPrice = crypto_prices[crypto.ticker]
        currentMarketValue = float(crypto.quantity) * spotPrice
        assetsGains.append(0 if float(currentMarketValue) < float(crypto.investment) else float(currentMarketValue) - float(crypto.investment))
        investments.append(float(crypto.investment))

    return investments, assetsGains

def get_crypto_price_data(tickers):
    all_symbols = " ".join(tickers)
    myInfo = Ticker(all_symbols)
    data = myInfo.price
    result = dict.fromkeys(data.keys())
    for key, value in data.items():
        result[key] = value['regularMarketPrice']
    return result

def crypto_list_view(request):
    cryptos = Crypto.objects.exclude(quantity=0)
    used_cryptos_ticker = cryptos.values_list('ticker', flat=True).distinct()
    crypto_prices = get_crypto_price_data(used_cryptos_ticker)
    investments, assetsGains = generate_bar_graph_series_data(cryptos, crypto_prices)

    transactions_table = []
    totalInvestment = 0
    totalMarketValue = 0

    for crypto in cryptos:
        spotPrice = crypto_prices[crypto.ticker]
        totalInvestment += crypto.investment
        currentMarketValue = float(crypto.quantity) * spotPrice
        totalMarketValue += currentMarketValue
        status = 'no-gain'
        if (float(currentMarketValue) - float(crypto.investment)) > 0 :
            status = 'profit'
        elif (float(currentMarketValue) - float(crypto.investment)) < 0:
            status = 'loss'
        transactions_table.append({
            "name": crypto.name,
            "ticker": crypto.ticker,
            "quantity": crypto.quantity,
            "totalInvestment": crypto.investment,
            "spotPrice": spotPrice,
            "currentMarketValue": currentMarketValue,
            "profit_loss_percentage": ((float(currentMarketValue) - float(crypto.investment)) / float(crypto.investment)) * 100 if crypto.investment > 0 else 'N/A',
            "status": status
        })

    context = {
        "transactions": transactions_table,
        "crypto_prices": crypto_prices,
        "totalInvestment": totalInvestment,
        "totalMarketValue": totalMarketValue,
        "usedCrypto": cryptos.values_list('name', flat=True).distinct(),
        "investments": investments,
        "assetsGains": assetsGains,
        "pie_chart_date": compute_pie_chart_transaction_types(cryptos, totalMarketValue, crypto_prices)

    }
    return render(request, "crypto/main.html", context)
def crypto_transactions(request, year=''):
    if year == '':
        transactions = CryptoTransaction.objects.all().order_by('date')
    else:
        transactions = CryptoTransaction.objects.filter(date__year=year).order_by('date')

    transactions_table = []
    for transaction in transactions:
        totalInvestment = float(transaction.quantity) * float(transaction.spot_price)
        transactions_table.append({
            "id": transaction.id,
            "crypto_name": transaction.coin,
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
    return render(request, "cryptoTransactions/transactions.html", context)

def add_crypto(request):
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

        form = CryptoForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.spot_price = spot_price
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
        else:
            form = CryptoForm
            if "submitted" in request.GET:
                submitted = True
        # else:
        #     messages.error(request, "This Ticker Spot price is not available!")
        #     return redirect("crypto:crypto-add")
    form = CryptoForm
    return render(request, "crypto/add.html", {"form": form, "submitted": submitted})


def update_crypto(request, pk):
    crypto = Crypto.objects.get(id=pk)
    form = CryptoForm(instance=crypto)

    if request.method == "POST":
        form = CryptoForm(request.POST, instance=crypto)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    context = {"form": form}
    return render(request, "crypto/add.html", context)


def delete_crypto(request, pk):
    crypto = Crypto.objects.get(id=pk)
    qs = Crypto.objects.get(id=pk)
    context = {
        "object": qs,
    }

    if request.method == "POST":
        crypto.delete()
        return HttpResponse('<script type="text/javascript">window.close()</script>')
    return render(request, "crypto/delete.html", context)

def add_transaction(request, **kwargs):
    submitted = False
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            if form.data["transaction_type"] == 'Buy':
                form.instance.coin.quantity += float(form.data["quantity"])
                form.instance.coin.investment += float(form.data["quantity"]) * float(form.data["spot_price"])
                form.instance.coin.save()
            else:
                form.instance.coin.quantity -= float(form.data["quantity"])
                if form.instance.coin.investment - float(form.data["quantity"]) * float(form.data["spot_price"]) < 0:
                    form.instance.coin.investment = float(0.0)
                else:
                    form.instance.coin.investment -= float(form.data["quantity"]) * float(form.data["spot_price"])
                form.instance.coin.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    else:
        form = TransactionForm
        if "submitted" in request.GET:
            submitted = True
    form = TransactionForm
    return render(
        request, "cryptoTransactions/add.html", {"form": form, "submitted": submitted}
    )


def update_transaction(request, pk):
    transaction = CryptoTransaction.objects.get(id=pk)
    form = TransactionForm(instance=transaction)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            if form.data["transaction_type"] == 'Buy':
                if form.cleaned_data["spot_price"]:
                    if form.cleaned_data["quantity"]:
                        form.instance.coin.quantity -= float(form.initial["quantity"])
                        form.instance.coin.quantity += float(form.cleaned_data["quantity"])
                        form.instance.coin.investment -= float(form.initial["quantity"]) * float(
                            form.initial["spot_price"])
                        form.instance.coin.investment += float(form.cleaned_data["quantity"]) * float(
                            form.cleaned_data["spot_price"])
                        form.instance.coin.save()
                    else:
                        form.instance.coin.investment -= float(form.initial["quantity"]) * float(
                            form.initial["spot_price"])
                        form.instance.coin.investment += float(form.initial["quantity"]) * float(
                            form.cleaned_data["spot_price"])
                        form.instance.coin.save()

                if form.cleaned_data["quantity"] and not form.cleaned_data["spot_price"]:
                    form.instance.coin.quantity -= float(form.initial["quantity"])
                    form.instance.coin.quantity += float(form.cleaned_data["quantity"])
                    form.instance.coin.investment -= float(form.initial["quantity"]) * float(
                        form.initial["spot_price"])
                    form.instance.coin.investment += float(form.cleaned_data["quantity"]) * float(
                        form.initial["spot_price"])
                    form.instance.coin.save()
                if form.cleaned_data["date"]:
                    form.instance.coin.date = form.cleaned_data["date"]

            else:
                if form.initial["spot_price"]:
                    if form.cleaned_data["quantity"]:
                        form.instance.coin.quantity -= float(form.initial["quantity"])
                        form.instance.coin.quantity += float(form.cleaned_data["quantity"])
                        form.instance.coin.investment += float(form.initial["quantity"]) * float(
                            form.initial["spot_price"])
                        form.instance.coin.investment -= float(form.cleaned_data["quantity"]) * float(
                            form.cleaned_data["spot_price"])
                    else:
                        form.instance.coin.investment += float(form.initial["quantity"]) * float(
                            form.initial["spot_price"])
                        form.instance.coin.investment -= float(form.initial["quantity"]) * float(
                            form.cleaned_data["spot_price"])

                    form.instance.coin.save()

                if form.cleaned_data["quantity"] and not form.cleaned_data["spot_price"]:
                    form.instance.coin.quantity -= float(form.initial["quantity"])
                    form.instance.coin.quantity += float(form.cleaned_data["quantity"])
                    form.instance.coin.investment += float(form.initial["quantity"]) * float(
                        form.initial["spot_price"])
                    form.instance.coin.investment -= float(form.cleaned_data["quantity"]) * float(
                        form.initial["spot_price"])
                    form.instance.coin.save()
                if form.cleaned_data["date"]:
                    form.instance.coin.date = form.cleaned_data["date"]
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    context = {"form": form}
    return render(request, "cryptoTransactions/add.html", context)


def delete_transaction(request, pk):
    transaction = CryptoTransaction.objects.get(id=pk)
    qs = CryptoTransaction.objects.get(id=pk)
    context = {
        "object": qs,
    }

    if request.method == "POST":
        # delete object
        if transaction.transaction_type == 'Buy':
            transaction.coin.quantity -= transaction.quantity
            transaction.coin.investment -= float(transaction.quantity) * float(transaction.spot_price)
            transaction.coin.save()
        else:
            transaction.coin.quantity += transaction.quantity
            transaction.coin.investment += float(transaction.quantity) * float(transaction.spot_price)
            transaction.coin.save()
        transaction.delete()
        # after deleting redirect to
        # home page
        return HttpResponse('<script type="text/javascript">window.close()</script>')

    return render(request, "cryptoTransactions/delete.html", context)
