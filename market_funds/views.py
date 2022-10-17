from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Trade, IndexFund
from .forms import IndexFundForm, TradeForm


def fund_list_view(request):
    qs = IndexFund.objects.all()
    total_value = 0
    for obj in qs:
        obj.value = round(obj.shares * obj.share_price, 2)
        total_value = total_value + obj.value
    context = {
        "object_list": qs,
        "total_value": total_value,
    }
    return render(request, "market_funds/main.html", context)


def add_indexfund(request):
    submitted = False
    if request.method == "POST":
        form = IndexFundForm(request.POST)
        if form.is_valid():
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
