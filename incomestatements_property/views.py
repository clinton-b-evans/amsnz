import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models.functions import TruncMonth, ExtractMonth

from django.db.models import Count, Sum, FloatField

from incomestatements.forms import CategoryForm
from incomestatements.models import Category
from .models import PropertyIncomeStatement, PropertyCategory
from properties.models import Property, Transactions
from .forms import PropertyIncomeStatementForm, PropertyCategoryForm
from copy import deepcopy


def incomestatement_property_list_view(request):
    property_list = request.GET.getlist("properties")

    prop_qs = Property.objects.all()
    if not property_list:
        qs = PropertyIncomeStatement.objects.all()
    else:
        qs = PropertyIncomeStatement.objects.filter(
            property__in=property_list
        ).order_by("-date")
    income_statement_list = PropertyIncomeStatement.objects.all().order_by("-date")
    total_income = 0
    total_expense = 0
    total = 0
    for item in qs:
        cat_qs = PropertyCategory.objects.get(name=item.propcategory)
        if cat_qs.transaction_type == "Income":
            total_income += item.amount
        else:
            total_expense += item.amount

    total = total_income - total_expense

    context = {
        "object_list": qs,
        "prop_qs": prop_qs,
        "income_statement_list": income_statement_list,
        "total": total,
    }
    return render(request, "propertyincomestatements/main.html", context)


def add_property_incomestatements(request):
    submitted = False
    if request.method == "POST":
        form = PropertyIncomeStatementForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    else:
        form = PropertyIncomeStatementForm
        if "submitted" in request.GET:
            submitted = True
    form = PropertyIncomeStatementForm
    return render(
        request,
        "propertyincomestatements/add.html",
        {"form": form, "submitted": submitted},
    )


def update_property_incomestatements(request, pk):
    propertyincomestatement = PropertyIncomeStatement.objects.get(id=pk)
    form = PropertyIncomeStatementForm(instance=propertyincomestatement)

    if request.method == "POST":
        form = PropertyIncomeStatementForm(
            request.POST, instance=propertyincomestatement
        )
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    context = {"form": form}
    return render(request, "incomestatements/add.html", context)


def delete_property_incomestatement(request, pk):
    propertyincomestatement = PropertyIncomeStatement.objects.get(id=pk)
    qs = PropertyIncomeStatement.objects.get(id=pk)
    context = {
        "object": qs,
    }

    if request.method == "POST":
        propertyincomestatement.delete()
        return HttpResponse('<script type="text/javascript">window.close()</script>')

    return render(request, "propertyincomestatements/delete.html", context)


def add_property_category(request):
    submitted = False
    if request.method == "POST":
        form = PropertyCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    else:
        form = PropertyCategoryForm
        if "submitted" in request.GET:
            submitted = True
    form = PropertyCategoryForm
    return render(
        request,
        "propertyincomestatements/add.html",
        {"form": form, "submitted": submitted},
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


def sort_years_list(myList):
    myList.sort(reverse=True)
    return myList


def year_to_date(request, year):
    years = PropertyIncomeStatement.objects.values_list("date__year").distinct()
    years_list = []
    for data in years:
        for item in data:
            years_list.append(item)
    years_list = sort_years_list(years_list)

    prop_qs = Property.objects.all()
    property_list = request.GET.getlist("properties")
    if not property_list:
        qs = PropertyIncomeStatement.objects.all()
    else:
        qs = PropertyIncomeStatement.objects.filter(
            property__in=property_list
        ).order_by("-date")

    qs = qs.filter(date__year=year)
    cat_dict = PropertyCategory.objects.all()
    categories = {}
    categories_total_yearly = {}

    """
    Display monthly total expenses for that time period
    """
    expense_qs = qs.filter(propcategory__transaction_type="Expense")
    income_qs = qs.filter(propcategory__transaction_type="Income")
    props_cat_monthly_expense_total = list(
        expense_qs.annotate(
            month=ExtractMonth("date"), total=Sum("amount", output_field=FloatField())
        ).values("month", "total")
    )
    props_cat_monthly_income_total = list(
        income_qs.annotate(
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

    # FOR PROPERTY MONTHLY EXPENSE
    for item in props_cat_monthly_expense_total:
        month = int(item["month"])
        month = datetime.datetime(int(year), month, 1)
        month = month.strftime("%B")
        item["month"] = month

    for item in props_cat_monthly_expense_total:
        for key in month_expenses.keys():
            if item["month"] == key:
                month_expenses[key] += item["total"]

    # FOR PROPERTY MONTHLY INCOME
    for item in props_cat_monthly_income_total:
        month = int(item["month"])
        month = datetime.datetime(int(year), month, 1)
        month = month.strftime("%B")
        item["month"] = month

    for item in props_cat_monthly_income_total:
        for key in month_income.keys():
            if item["month"] == key:
                month_income[key] += item["total"]

    # CATEGORIES EACH MONTH TOTAL EXPENSES
    monthly_data = {
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
    unique_categories_of_expenses = expense_qs.values("propcategory__name").distinct()
    result = {}
    for category in unique_categories_of_expenses:
        result[f"{list(category.values())[0]}"] = {
            "months": deepcopy(monthly_data),
            "total": 0,
        }

    for month in monthly_data.keys():
        current_month_total_expense = 0
        month_int = datetime.datetime.strptime(month, "%B").month
        current_month_expenses = expense_qs.filter(date__month=month_int)
        print(month, current_month_expenses)
        for expense_in_current_month in current_month_expenses:
            current_month_total_expense += expense_in_current_month.amount
            category_of_expense = PropertyCategory.objects.get(
                name=expense_in_current_month.propcategory
            )
            result[f"{category_of_expense}"]["months"][f"{month}"] = float(
                current_month_total_expense
            )

    for category in unique_categories_of_expenses:
        result[f"{list(category.values())[0]}"]["total"] = sum(
            result[f"{list(category.values())[0]}"]["months"].values()
        )
        print(result)
        print(sum(result[f"{list(category.values())[0]}"]["months"].values()))
    # END OF CATEGORIES EACH MONTH TOTAL EXPENSES

    # Yearly Summation of each category expense
    for item in cat_dict:
        categories_total_yearly[item.name] = 0
        categories[item.name] = 0
    for item in qs:
        cat_qs = PropertyCategory.objects.get(name=item.propcategory)
        if cat_qs.name in categories_total_yearly:
            categories_total_yearly[cat_qs.name] += item.amount

    categories_lists = list(categories.keys())

    total_income = 0
    total_expense = 0
    for item in qs:
        cat_qs = PropertyCategory.objects.get(name=item.propcategory)
        if cat_qs.transaction_type == "Income":
            total_income += item.amount
        else:
            total_expense += item.amount

    total = total_income - total_expense
    category_total_yearly = {x: y for x, y in categories_total_yearly.items() if y != 0}

    context = {
        "object_list": qs,
        "year": year,
        "total": total,
        "income": total_income,
        "expense": total_expense,
        "categories_yearly": category_total_yearly,
        "categories_lists": categories_lists,
        "month_expenses": month_expenses,
        "month_income": month_income,
        "prop_qs": prop_qs,
        "years_list": years_list,
    }
    return render(request, "propertyincomestatements/ytd.html", context)
