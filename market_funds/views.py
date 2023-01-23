from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from .models import Trade, IndexFund
from .forms import IndexFundForm, TradeForm
import yfinance as yf
from datetime import date


def sort(myList):
    myList.sort()
    return myList


@login_required(login_url='/login/')
def fund_list_view(request, year):
    index_fund_list_object = IndexFund.objects.filter(date__year=year)
    total_value = 0
    for fund in index_fund_list_object:
        fund.value = round(fund.shares * fund.share_price, 2)
        total_value = total_value + fund.value

    years = list(IndexFund.objects.values_list("date__year").distinct())
    years_list = []
    for data in years:
        for item in data:
            years_list.append(item)
    years_list = sort(years_list)

    # Yearly date collection
    index_fund_all_years_total_list = []
    total_value_yearly = 0
    for my_year in years_list:
        index_fund_list_objects = IndexFund.objects.filter(date__year=my_year)
        for fund in index_fund_list_objects:
            fund.value = round(fund.shares * fund.share_price, 2)
            total_value_yearly = total_value_yearly + fund.value
        index_fund_all_years_total_list.append(float(total_value_yearly))
    context = {
        "index_fund_list_object": index_fund_list_object,
        "total_value": total_value,
        "years_list": years_list,
        "index_fund_all_years_total_list": index_fund_all_years_total_list,
        "year": year,
    }
    return render(request, "market_funds/main.html", context)


def add_indexfund(request):
    today = date.today().isoformat()
    submitted = False
    if request.method == "POST":
        ticker = request.POST.get("ticker")
        yf_data = yf.Ticker(ticker)
        yf_data = yf_data.history(today, interval="60m")
        share_price = 0
        if yf_data["Close"].empty:
            return HttpResponse(
                f"-{ticker} No data found, symbol/Ticker may be de-listed!. Kindly try again with correct Ticker."
            )
        else:
            last_price = yf_data["Close"][0]
            string_price = "{:.4f}".format(last_price)
            share_price += float(string_price)

        form = IndexFundForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.share_price = share_price
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    else:
        form = IndexFundForm
        if "submitted" in request.GET:
            submitted = True
    form = IndexFundForm
    return render(
        request, "market_funds/add.html", {"form": form, "submitted": submitted}
    )


def update_indexfund(request, pk):
    indexfund = IndexFund.objects.get(id=pk)
    form = IndexFundForm(instance=indexfund)

    if request.method == "POST":
        form = IndexFundForm(request.POST, instance=indexfund)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    context = {"form": form}
    return render(request, "market_funds/add.html", context)


def delete_indexfund(request, pk):
    indexfund = IndexFund.objects.get(id=pk)
    qs = IndexFund.objects.get(id=pk)
    context = {
        "object": qs,
    }

    if request.method == "POST":
        # delete object
        indexfund.delete()
        # after deleting redirect to
        # home page
        return HttpResponse('<script type="text/javascript">window.close()</script>')
    return render(request, "market_funds/delete.html", context)


def add_trade(request):
    submitted = False
    if request.method == "POST":
        form = TradeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    else:
        form = TradeForm
        if "submitted" in request.GET:
            submitted = True
    form = TradeForm
    return render(request, "trades/add.html", {"form": form, "submitted": submitted})


@login_required(login_url='/login/')
def indexfund_detail_view(request, **kwargs):
    pk = kwargs.get("pk")
    obj = IndexFund.objects.get(pk=pk)
    tradeobj = Trade.objects.filter(indexfund=obj)
    for printthis in tradeobj:
        print(printthis.date)

    context = {
        "tradeobj": tradeobj,
    }
    return render(request, "market_funds/detail.html", context)
