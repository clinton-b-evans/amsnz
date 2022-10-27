import datetime
from copy import deepcopy
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
    myList.sort()
    return myList


def year_to_date(request, year):
    qs = IncomeStatement.objects.filter(date__year=year)
    cat_dict = Category.objects.all()
    expense_qs = qs.filter(category__transaction_type="Expense")

    categories_expense_yearly = {}
    for item in cat_dict:
        categories_expense_yearly[item.name] = 0
    for item in expense_qs:
        cat_qs = Category.objects.get(name=item.category)
        if cat_qs.name in categories_expense_yearly:
            categories_expense_yearly[cat_qs.name] += item.amount
        else:
            print("Here is thing")
    categories_expense_yearly = {
        x: y for x, y in categories_expense_yearly.items() if y != 0
    }

    total_income = 0
    total_expense = 0
    for item in qs:
        cat_qs = Category.objects.get(name=item.category)
        if cat_qs.transaction_type == "Income":
            total_income += item.amount
        else:
            total_expense += item.amount

    net_amount = total_income - total_expense

    # START EACH YEAR MONTHLY EXPENSES CALCULATIONS
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
    total_expense = 0
    for month, amount in month_expenses.items():
        total_expense += amount
    month_expenses.update({"total": total_expense})
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
    total_income = 0
    for month, amount in month_income.items():
        total_income += amount
    month_income.update({"total": total_income})
    # END OF EACH YEAR MONTHLY INCOME CALCULATIONS

    # CATEGORIES EACH MONTH TOTAL Income
    monthly_income_data = {
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
    unique_categories_of_income = income_qs.values("category__name").distinct()
    income_result = {}
    for category in unique_categories_of_income:
        income_result[f"{list(category.values())[0]}"] = {
            "months": deepcopy(monthly_income_data),
            "total": 0,
        }

    for month in monthly_income_data.keys():
        current_month_total_income = 0
        month_int = datetime.datetime.strptime(month, "%B").month
        current_month_income = income_qs.filter(date__month=month_int)
        # print(month, current_month_income)
        for income_in_current_month in current_month_income:
            current_month_total_income += income_in_current_month.amount
            category_of_income = Category.objects.get(
                name=income_in_current_month.category
            )
            income_result[f"{category_of_income}"]["months"][f"{month}"] = float(
                current_month_total_income
            )

    for category in unique_categories_of_income:
        income_result[f"{list(category.values())[0]}"]["total"] = sum(
            income_result[f"{list(category.values())[0]}"]["months"].values()
        )
    # #### END OF CATEGORIES EACH MONTH TOTAL Income ####

    # START CATEGORIES EACH MONTH TOTAL EXPENSES
    monthly_expenses_data = {
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
    unique_categories_of_expenses = expense_qs.values("category__name").distinct()
    expenses_result = {}
    for category_expense in unique_categories_of_expenses:
        expenses_result[f"{list(category_expense.values())[0]}"] = {
            "months": deepcopy(monthly_expenses_data),
            "total": 0,
        }

    for month in monthly_expenses_data.keys():
        current_month_total_expense = 0
        month_int = datetime.datetime.strptime(month, "%B").month
        current_month_expenses = expense_qs.filter(date__month=month_int)
        # print(month, current_month_expenses)
        for expense_in_current_month in current_month_expenses:
            current_month_total_expense += expense_in_current_month.amount
            category_of_expense = Category.objects.get(
                name=expense_in_current_month.category
            )
            expenses_result[f"{category_of_expense}"]["months"][f"{month}"] = float(
                current_month_total_expense
            )

    for category_expense in unique_categories_of_expenses:
        expenses_result[f"{list(category_expense.values())[0]}"]["total"] = sum(
            expenses_result[f"{list(category_expense.values())[0]}"]["months"].values()
        )
    #  #### END OF CATEGORIES EACH MONTH TOTAL EXPENSES ####

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
        "categories_expense_yearly": categories_expense_yearly,
        "years_list": years_list,
        "income_result": income_result,
        "expenses_result": expenses_result,
    }
    return render(request, "incomestatements/ytd.html", context)
