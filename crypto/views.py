import json
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from yahooquery import Ticker

from incomestatements_property.views import sort_years_list
from .models import Crypto, CryptoTransaction, CrudUser
from .forms import CryptoForm, TransactionForm
import yfinance as yf
from datetime import date, timedelta


def crudview(request):
    model = CrudUser.objects.all().values()
    context = {'username': 'qadeer', 'users': model}
    return render(request, "cryptoTransactions/crud.html", context)


def get(request):
    name1 = request.GET.get('name', None)
    address1 = request.GET.get('address', None)
    age1 = request.GET.get('age', None)

    obj = CrudUser.objects.create(
        name=name1,
        address=address1,
        age=age1
    )

    user = {'id': obj.id, 'name': obj.name, 'address': obj.address, 'age': obj.age}

    data = {
        'user': user
    }
    return JsonResponse(data)


def update(request):
    id1 = request.GET.get('id', None)
    name1 = request.GET.get('name', None)
    address1 = request.GET.get('address', None)
    age1 = request.GET.get('age', None)

    obj = CrudUser.objects.get(id=id1)
    obj.name = name1
    obj.address = address1
    obj.age = age1
    obj.save()

    user = {'id': obj.id, 'name': obj.name, 'address': obj.address, 'age': obj.age}

    data = {
        'user': user
    }
    return JsonResponse(data)


def compute_pie_chart_transaction_types(cryptos, totalMarketValue, crypto_prices):
    pie_chart_data = []
    for crypto in cryptos:
        if crypto.quantity > 0:
            percentage = ((float(crypto.quantity) * float(crypto_prices[crypto.ticker])) / totalMarketValue) * 100
        else:
            percentage = 0
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
        currentMarketValue = float(crypto.quantity) * float(spotPrice)
        assetsGains.append(
            0 if float(currentMarketValue) < float(crypto.investment) else float(currentMarketValue) - float(
                crypto.investment))
        investments.append(float(crypto.investment))

    return investments, assetsGains


def get_crypto_price_data(tickers):
    all_symbols = " ".join(tickers)
    myInfo = Ticker(all_symbols)
    data = myInfo.price
    result = dict.fromkeys(data.keys())
    print(data, 'data')
    for key, value in data.items():
        result[key] = value['regularMarketPrice']
        print(result, 'result')
    return result


@login_required(login_url='/login/')
def crypto_list_view(request, year):
    cryptos = Crypto.objects.filter(user=request.user).exclude(quantity=0)
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
        if (float(currentMarketValue) - float(crypto.investment)) > 0:
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
            "profit_loss_percentage": ((float(currentMarketValue) - float(crypto.investment)) / float(
                crypto.investment)) * 100 if crypto.investment > 0 else 'N/A',
            "status": status
        })
    my_investments_list = ['%.2f' % elem for elem in investments]
    my_assetsGains_list = ['%.2f' % elem for elem in assetsGains]
    years = CryptoTransaction.objects.values_list("date__year").distinct()
    years_list = []
    for data in years:
        for item in data:
            years_list.append(item)
    years_list = sort_years_list(years_list)
    context = {
        "transactions": transactions_table,
        "crypto_prices": crypto_prices,
        "totalInvestment": totalInvestment,
        "totalMarketValue": totalMarketValue,
        "usedCrypto": cryptos.values_list('name', flat=True).distinct(),
        "investments": list(map(float, my_investments_list)),
        "assetsGains": list(map(float, my_assetsGains_list)),
        "pie_chart_date": compute_pie_chart_transaction_types(cryptos, totalMarketValue, crypto_prices),
        "years_list":years_list
    }
    return render(request, "crypto/main.html", context)


@login_required(login_url='/login/')
def crypto_transactions(request, year):
    crypto_coin = Crypto.objects.filter(user=request.user).values()
    if year == '':
        transactions = CryptoTransaction.objects.filter(user=request.user).order_by('date')
    else:
        transactions = CryptoTransaction.objects.filter(date__year=year, user=request.user).order_by('date')

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
    years = CryptoTransaction.objects.values_list("date__year").distinct()
    years_list = []
    for data in years:
        for item in data:
            years_list.append(item)
    years_list = sort_years_list(years_list)
    context = {
        "year": year,
        "transactions": transactions_table,
        "form": TransactionForm,
        "crypto": crypto_coin,
        "years_list": years_list,
    }
    return render(request, "cryptoTransactions/transactions.html", context)


# def add_crypto(request):
#     today = date.today().isoformat()
#
#     submitted = False
#     if request.method == "POST":
#         ticker_input = request.POST.get("ticker")
#         ticker = ticker_input + "-USD"
#
#         yf_data = yf.Ticker(ticker)
#         yf_data = yf_data.history(today, interval="60m")
#         spot_price = 0.0
#
#         if yf_data["Close"].empty:
#             return HttpResponse(
#                 f"-{ticker_input} No data found, symbol/Ticker may be de-listed!. Kindly try again with correct Ticker."
#             )
#         else:
#             last_price = yf_data["Close"][0]
#             string_price = "{:.4f}".format(last_price)
#             spot_price += float(string_price)
#
#         form = CryptoForm(request.POST)
#         if form.is_valid():
#             form = form.save(commit=False)
#             form.spot_price = spot_price
#             form.save()
#             return HttpResponse(
#                 '<script type="text/javascript">window.close()</script>'
#             )
#         else:
#             form = CryptoForm
#             if "submitted" in request.GET:
#                 submitted = True
#         # else:
#         #     messages.error(request, "This Ticker Spot price is not available!")
#         #     return redirect("crypto:crypto-add")
#     form = CryptoForm
#     return render(request, "crypto/add.html", {"form": form, "submitted": submitted})


def update_crypto(request, pk):
    crypto = Crypto.objects.get(id=pk, user=request.user)
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
    crypto = Crypto.objects.get(id=pk, user=request.user)
    qs = Crypto.objects.get(id=pk, user=request.user)
    context = {
        "object": qs,
    }

    if request.method == "POST":
        crypto.delete()
        return HttpResponse('<script type="text/javascript">window.close()</script>')
    return render(request, "crypto/delete.html", context)


def add_crypto(request):
    if request.method == "POST":
        # getting body data from request
        cryptoData = json.loads(request.body)
        obj = Crypto.objects.create(
            name=cryptoData['coin'],
            ticker=cryptoData['ticker'],
            user=request.user
        )

        user = {'id': obj.id, 'ticker': obj.ticker, 'name': obj.name}

        data = {
            'user': user
        }
        return JsonResponse(data)


def add_transaction(request):
    if request.method == "POST":
        # getting body data from request
        transactionData = json.loads(request.body)
        # getting models
        crypto = Crypto.objects.get(name=transactionData['coin'], user=request.user)
        # saving data to crypto model
        # when transactions_type is buy
        if transactionData["transaction_type"] == 'Buy':
            crypto.quantity += float(transactionData["quantity"])
            crypto.investment += float(transactionData["quantity"]) * float(transactionData["spot_price"])
            crypto.save()
        # when transactions_type is sell
        else:
            if crypto.quantity - float(transactionData["quantity"]) > -1:
                crypto.quantity -= float(transactionData["quantity"])
                if crypto.investment - (float(transactionData["quantity"]) * float(transactionData["spot_price"])) < 0:
                    crypto.investment = float(0.0)
                    print("working")
                else:
                    crypto.investment -= float(transactionData["quantity"]) * float(transactionData["spot_price"])
                    print("not working")
                crypto.save()
            else:
                data = {
                    "quantity": "error"
                }
                return JsonResponse(data)
        obj = CryptoTransaction.objects.create(
            coin=Crypto.objects.get(name=transactionData["coin"],user=request.user ),
            transaction_type=transactionData['transaction_type'],
            quantity=transactionData['quantity'],
            spot_price=transactionData['spot_price'],
            date=transactionData['date'],
            user=request.user
        )
        user = {
            'id': obj.id,
            'coin': transactionData['coin'],
            'spot_price': obj.spot_price,
            'transaction_type': obj.transaction_type,
            'quantity': obj.quantity,
            'date': obj.date
        }
        data = {
            'user': user
        }
        print(data, 'data')
        return JsonResponse(data)


# def add_transaction(request):
#     if request.method == "POST":
#         form = TransactionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             if form.data["transaction_type"] == 'Buy':
#                 form.instance.coin.quantity += float(form.data["quantity"])
#                 form.instance.coin.investment += float(form.data["quantity"]) * float(form.data["spot_price"])
#                 form.instance.coin.save()
#             else:
#                 form.instance.coin.quantity -= float(form.data["quantity"])
#                 if form.instance.coin.investment - float(form.data["quantity"]) * float(form.data["spot_price"]) < 0:
#                     form.instance.coin.investment = float(0.0)
#                 else:
#                     form.instance.coin.investment -= float(form.data["quantity"]) * float(form.data["spot_price"])
#                 form.instance.coin.save()
#             return HttpResponse(
#                 '<script type="text/javascript">window.close()</script>'
#             )
#         return True
#     else:
#         return False


def edit_transaction(request):
    if request.method == "POST":
        # getting body data from request
        data = json.loads(request.body)
        # setting the id
        pk = data['transactionId']
        # getting models
        transaction = CryptoTransaction.objects.get(id=pk, user=request.user)
        crypto = Crypto.objects.get(name=data['coin'], user=request.user)
        print(crypto.investment, 'crypto')
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
                    crypto.quantity -= float(transaction.quantity)
                    crypto.quantity += float(data["quantity"])
                    crypto.investment -= float(transaction.quantity) * float(
                        transaction.spot_price)
                    crypto.investment += float(data["quantity"]) * float(
                        data["spot_price"])
                    crypto.save()
                else:
                    crypto.investment -= float(transaction.quantity) * float(
                        transaction.spot_price)
                    crypto.investment += float(transaction.quantity) * float(
                        data["spot_price"])
                    crypto.save()
            # if quantity changed and spotPrice didn't change
            if data["quantity"] != transaction.quantity and data["spot_price"] == transaction.spot_price:
                crypto.quantity -= float(transaction.quantity)
                crypto.quantity += float(data["quantity"])
                crypto.investment -= float(transaction.quantity) * float(
                    transaction.spot_price)
                crypto.investment += float(data["quantity"]) * float(
                    transaction.spot_price)
                crypto.save()
        # when transactions_type is sell
        else:
            # if spot_price changed
            if data["spot_price"] != transaction.spot_price:
                # if quantity changed
                if data["quantity"] != transaction.quantity:
                    crypto.quantity -= float(transaction.quantity)
                    crypto.quantity += float(data["quantity"])
                    crypto.investment += float(transaction.quantity) * float(
                        transaction.spot_price)
                    crypto.investment -= float(data["quantity"]) * float(
                        data["spot_price"])
                else:
                    crypto.investment += float(transaction.quantity) * float(
                        transaction.spot_price)
                    crypto.investment -= float(transaction.quantity) * float(
                        data["spot_price"])
                crypto.save()
            # if quantity changed and spotPrice didn't change
            if data["quantity"] != transaction.quantity and data["spot_price"] == transaction.spot_price:
                crypto.quantity -= float(transaction.quantity)
                crypto.quantity += float(data["quantity"])
                crypto.investment += float(transaction.quantity) * float(
                    transaction.spot_price)
                crypto.investment -= float(data["quantity"]) * float(
                    transaction.spot_price)
                crypto.save()
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


def update_transaction(request, pk):
    transaction = CryptoTransaction.objects.get(id=pk, user=request.user)
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


def delete_transaction(request):
    id1 = request.GET.get('id', None)
    transaction = CryptoTransaction.objects.get(id=id1, user=request.user)
    if transaction.transaction_type == 'Buy':
        transaction.coin.quantity -= transaction.quantity
        transaction.coin.investment -= float(transaction.quantity) * float(transaction.spot_price)
        transaction.coin.save()
        print('buy')
    else:
        transaction.coin.quantity += transaction.quantity
        transaction.coin.investment += float(transaction.quantity) * float(transaction.spot_price)
        transaction.coin.save()
        print('sell')
    CryptoTransaction.objects.get(id=id1, user=request.user).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)

# def delete_transaction(request, pk):
#     transaction = CryptoTransaction.objects.get(id=pk)
#     qs = CryptoTransaction.objects.get(id=pk)
#     context = {
#         "object": qs,
#     }
#
#     if request.method == "POST":
#         # delete object
#         if transaction.transaction_type == 'Buy':
#             transaction.coin.quantity -= transaction.quantity
#             transaction.coin.investment -= float(transaction.quantity) * float(transaction.spot_price)
#             transaction.coin.save()
#         else:
#             transaction.coin.quantity += transaction.quantity
#             transaction.coin.investment += float(transaction.quantity) * float(transaction.spot_price)
#             transaction.coin.save()
#         transaction.delete()
#         # after deleting redirect to
#         # home page
#         return HttpResponse('<script type="text/javascript">window.close()</script>')
#
#     return render(request, "cryptoTransactions/delete.html", context)
