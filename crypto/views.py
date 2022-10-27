import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Crypto
from .forms import CryptoForm
from django.contrib import messages

CRYPTO_API_KEY = "HBOtOtoU9lxxj6k0T1ybf6i"


def sort(myList):
    myList.sort()
    return myList


def crypto_list_view(request, year):
    crypto_objects_lists = Crypto.objects.filter(date__year=year)
    total = 0
    for obj in crypto_objects_lists:
        obj.total = round(obj.qty * obj.spot_price, 2)
        total = total + obj.total
    total_amounts = 0

    for crypto in crypto_objects_lists:
        total_amounts += crypto.total

    for crypto_per in crypto_objects_lists:
        crypto_per.percent = (crypto_per.total / total_amounts) * 100

    years = list(Crypto.objects.values_list("date__year").distinct())
    years_list = []
    for each in years:
        for item in each:
            years_list.append(item)
    years_list = sort(years_list)

    crypto_all_years_total_list = []
    # crypto_total = 0
    for my_year in years_list:
        crypto_objects = Crypto.objects.filter(date__year=my_year)
        crypto_total = 0
        for obj in crypto_objects:
            obj.total = round(obj.qty * obj.spot_price, 2)
            crypto_total = crypto_total + obj.total
        grand_total = 0
        for item in crypto_objects:
            grand_total += item.total
        for item in crypto_objects:
            item.percent = (item.total / grand_total) * 100
        crypto_all_years_total_list.append(float(crypto_total))
        print("crypto_total", crypto_total)
    print("all_years_crypto_total", crypto_all_years_total_list)
    context = {
        "crypto_objects_lists": crypto_objects_lists,
        "total": total,
        "years_list": years_list,
        "crypto_all_years_total_list": crypto_all_years_total_list,
        "year": year,
    }
    return render(request, "crypto/main.html", context)


def add_crypto(request):
    submitted = False
    if request.method == "POST":
        ticker = request.POST.get("ticker")
        url = f"https://fcsapi.com/api-v3/crypto/latest?symbol={ticker}/usd&access_key=HBOtOtoU9lxxj6k0T1ybf6i"
        response = requests.request("GET", url)
        result = response.json()

        spot_price = 0.0
        if result["status"]:
            for price in result["response"][:1]:
                spot_price = price["c"]
            spot_price = float(spot_price)
        else:
            return HttpResponse(
                "No ticker data or an invalid value has been specified, Data not found "
            )

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
