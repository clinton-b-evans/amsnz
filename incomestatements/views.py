import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import IncomeStatement, Category
from .forms import IncomeStatementForm, CategoryForm
from django.db.models.functions import TruncMonth, ExtractMonth
from django.db.models import Count, Sum, FloatField


def incomestatements_list_view(request):
    qs = IncomeStatement.objects.all()
    total_income = 0
    total_expense = 0
    total = 0
    for item in qs:
        cat_qs = Category.objects.get(name=item.category)
        if cat_qs.transaction_type == "Income":
            total_income += item.amount
        else:
            total_expense += item.amount

    total = total_income - total_expense

    context = {
        "object_list": qs,
        "total": total,
    }
    return render(request, "incomestatements/main.html", context)


def add_incomestatements(request):
    submitted = False
    if request.method == "POST":
        form = IncomeStatementForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    else:
        form = IncomeStatementForm
        if "submitted" in request.GET:
            submitted = True
    form = IncomeStatementForm
    return render(
        request, "incomestatements/add.html", {"form": form, "submitted": submitted}
    )


def update_incomestatements(request, pk):
    incomestatement = IncomeStatement.objects.get(id=pk)
    form = IncomeStatementForm(instance=incomestatement)

    if request.method == "POST":
        form = IncomeStatementForm(request.POST, instance=incomestatement)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    context = {"form": form}
    return render(request, "incomestatements/add.html", context)


def delete_incomestatement(request, pk):
    incomestatement = IncomeStatement.objects.get(id=pk)
    qs = IncomeStatement.objects.get(id=pk)
    context = {
        "object": qs,
    }

    if request.method == "POST":
        # delete object
        incomestatement.delete()
        # after deleting redirect to
        # home page
        return HttpResponse('<script type="text/javascript">window.close()</script>')

    return render(request, "incomestatements/delete.html", context)


def add_category(request):
    submitted = False
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    else:
        form = CategoryForm
        if "submitted" in request.GET:
            submitted = True
    form = CategoryForm
    return render(
        request, "incomestatements/add.html", {"form": form, "submitted": submitted}
    )


def update_category(request, pk):
    category = Category.objects.get(id=pk)
    form = CategoryForm(instance=category)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    context = {"form": form}
    return render(request, "incomestatements/add.html", context)


def sort(myList):
    myList.sort(reverse=True)
    return myList


def year_to_date(request, year):
    qs = IncomeStatement.objects.filter(date__year=year)
    cat_dict = Category.objects.all()
    categories = {}
    for item in cat_dict:
        categories[item.name] = 0
    for item in qs:
        cat_qs = Category.objects.get(name=item.category)
        if cat_qs.name in categories:
            categories[cat_qs.name] += item.amount
        else:
            print("Here is thing")
    total_income = 0
    total_expense = 0
    total = 0
    for item in qs:
        cat_qs = Category.objects.get(name=item.category)
        if cat_qs.transaction_type == "Income":
            total_income += item.amount
        else:
            total_expense += item.amount

    net_amount = total_income - total_expense

    # START EACH YEAR MONTHLY EXPENSES CALCULATIONS
    expense_qs = qs.filter(category__transaction_type="Expense")
    props_cat_monthly_expense_total = list(
        expense_qs.annotate(
            month=ExtractMonth("date"), total=Sum("amount", output_field=FloatField())
        ).values("month", "total")
    )
    month_expenses = {
        "January": 0,
        "February": 0,
        "March": 0,
        "April": 0,
        "May": 0,
        "June": 0,
        "July": 0,
        "August": 0,
        "September": 0,
        "October": 0,
        "November": 0,
        "December": 0,
    }
    for item in props_cat_monthly_expense_total:
        month = int(item["month"])
        month = datetime.datetime(int(year), month, 1)
        month = month.strftime("%B")
        item["month"] = month

    for item in props_cat_monthly_expense_total:
        for key in month_expenses.keys():
            if item["month"] == key:
                month_expenses[key] += item["total"]
    #  ### END OF EACH YEAR MONTHLY EXPENSES CALCULATIONS ###

    # START OF EACH YEAR MONTHLY INCOME CALCULATIONS
    income_qs = qs.filter(category__transaction_type="Income")
    props_cat_monthly_income_total = list(
        income_qs.annotate(
            month=ExtractMonth("date"), total=Sum("amount", output_field=FloatField())
        ).values("month", "total")
    )
    month_income = {
        "January": 0,
        "February": 0,
        "March": 0,
        "April": 0,
        "May": 0,
        "June": 0,
        "July": 0,
        "August": 0,
        "September": 0,
        "October": 0,
        "November": 0,
        "December": 0,
    }
    for item in props_cat_monthly_income_total:
        month = int(item["month"])
        month = datetime.datetime(int(year), month, 1)
        month = month.strftime("%B")
        item["month"] = month

    for item in props_cat_monthly_income_total:
        for key in month_income.keys():
            if item["month"] == key:
                month_income[key] += item["total"]
    # END OF EACH YEAR MONTHLY INCOME CALCULATIONS

    yearly_expenses_categories = {x: y for x, y in categories.items() if y != 0}
    years = list(IncomeStatement.objects.values_list("date__year").distinct())
    years_list = []
    for each in years:
        for item in each:
            years_list.append(item)
    years_list = sort(years_list)
    context = {
        "object_list": qs,
        "year": year,
        "total_income": total_income,
        "total_expense": total_expense,
        "total_amount": net_amount,
        "month_expenses": month_expenses,
        "month_income": month_income,
        "categories": yearly_expenses_categories,
        "years_list": years_list,
    }
    return render(request, "incomestatements/ytd.html", context)
