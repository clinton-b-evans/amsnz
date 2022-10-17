from django.shortcuts import render
from .models import CashFlow
from .forms import CashFlowForm
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def cash_flow_list_view(request):
    selected = "Monthly"
    qs_income = CashFlow.objects.filter(entry_type="Income")
    qs_expense = CashFlow.objects.filter(entry_type="Expense")
    total_income = 0
    total_expense = 0

    for item in qs_income:
        if item.frequency == "Weekly":
            item.amount = item.amount * 52 / 12
            item.amount = round(item.amount, 2)
        elif item.frequency == "Fortnightly":
            item.amount = item.amount * 26 / 12
            item.amount = round(item.amount, 2)
        elif item.frequency == "Yearly":
            item.amount = item.amount / 12
            item.amount = round(item.amount, 2)
        total_income = total_income + item.amount

    for item in qs_expense:
        if item.frequency == "Weekly":
            item.amount = item.amount * 52 / 12
            item.amount = round(item.amount, 2)
        elif item.frequency == "Fortnightly":
            item.amount = item.amount * 26 / 12
            item.amount = round(item.amount, 2)
        elif item.frequency == "Yearly":
            item.amount = item.amount / 12
            item.amount = round(item.amount, 2)
        total_expense = total_expense + item.amount

    cashflow = total_income - total_expense

    if cashflow > 0:
        cashflow_class = "black"
    else:
        cashflow_class = "red"
    context = {
        "income": qs_income,
        "expense": qs_expense,
        "total_income": total_income,
        "total_expense": total_expense,
        "cashflow": cashflow,
        "cashflow_class": cashflow_class,
        "selected": selected,
    }
    return render(request, "cash_flows/main.html", context)


def cash_flow_weekly_view(request):
    selected = "Weekly"
    qs_income = CashFlow.objects.filter(entry_type="Income")
    qs_expense = CashFlow.objects.filter(entry_type="Expense")
    total_income = 0
    total_expense = 0

    for item in qs_income:
        if item.frequency == "Monthly":
            item.amount = item.amount * 12 / 52
            item.amount = round(item.amount, 2)
        elif item.frequency == "Fortnightly":
            item.amount = item.amount * 26 / 52
            item.amount = round(item.amount, 2)
        elif item.frequency == "Yearly":
            item.amount = item.amount / 52
            item.amount = round(item.amount, 2)
        total_income = total_income + item.amount

    for item in qs_expense:
        if item.frequency == "Monthly":
            item.amount = item.amount * 12 / 52
            item.amount = round(item.amount, 2)
        elif item.frequency == "Fortnightly":
            item.amount = item.amount * 26
            item.amount = round(item.amount, 2)
        elif item.frequency == "Yearly":
            item.amount = item.amount / 52
            item.amount = round(item.amount, 2)
        total_expense = total_expense + item.amount

    cashflow = total_income - total_expense

    if cashflow > 0:
        cashflow_class = "black"
    else:
        cashflow_class = "red"
    context = {
        "income": qs_income,
        "expense": qs_expense,
        "total_income": total_income,
        "total_expense": total_expense,
        "cashflow": cashflow,
        "cashflow_class": cashflow_class,
        "selected": selected,
    }
    return render(request, "cash_flows/main.html", context)


def cash_flow_yearly_view(request):
    selected = "Yearly"
    qs_income = CashFlow.objects.filter(entry_type="Income")
    qs_expense = CashFlow.objects.filter(entry_type="Expense")
    total_income = 0
    total_expense = 0

    for item in qs_income:
        if item.frequency == "Weekly":
            item.amount = item.amount * 52
            item.amount = round(item.amount, 2)
        elif item.frequency == "Monthly":
            item.amount = item.amount * 12
            item.amount = round(item.amount, 2)
        elif item.frequency == "Fortnightly":
            item.amount = item.amount * 26
            item.amount = round(item.amount, 2)
        total_income = total_income + item.amount

    for item in qs_expense:
        if item.frequency == "Weekly":
            item.amount = item.amount * 52
            item.amount = round(item.amount, 2)
        elif item.frequency == "Monthly":
            item.amount = item.amount * 12
            item.amount = round(item.amount, 2)
        elif item.frequency == "Fortnightly":
            item.amount = item.amount * 26
            item.amount = round(item.amount, 2)
        total_expense = total_expense + item.amount

    cashflow = total_income - total_expense

    if cashflow > 0:
        cashflow_class = "black"
    else:
        cashflow_class = "red"
    context = {
        "income": qs_income,
        "expense": qs_expense,
        "total_income": total_income,
        "total_expense": total_expense,
        "cashflow": cashflow,
        "cashflow_class": cashflow_class,
        "selected": selected,
    }
    return render(request, "cash_flows/main.html", context)


def add_cash_flow(request):
    submitted = False
    if request.method == "POST":
        form = CashFlowForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    else:
        form = CashFlowForm
        if "submitted" in request.GET:
            submitted = True
    form = CashFlowForm
    return render(
        request, "cash_flows/add.html", {"form": form, "submitted": submitted}
    )


def update_cash_flow(request, pk):
    cash_flow = CashFlow.objects.get(id=pk)
    form = CashFlowForm(instance=cash_flow)

    if request.method == "POST":
        form = CashFlowForm(request.POST, instance=cash_flow)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    context = {"form": form}
    return render(request, "cash_flows/add.html", context)


def delete_cash_flow(request, pk):
    cash_flow = CashFlow.objects.get(id=pk)
    qs = CashFlow.objects.get(id=pk)
    context = {
        "object": qs,
    }

    if request.method == "POST":
        # delete object
        cash_flow.delete()
        # after deleting redirect to
        # home page
        return HttpResponse('<script type="text/javascript">window.close()</script>')

    return render(request, "cash_flows/delete.html", context)
