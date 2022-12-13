import datetime
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models.functions import TruncMonth, ExtractMonth

from django.db.models import Count, Sum, FloatField

from incomestatements.forms import CategoryForm
from incomestatements.models import Category
from .models import PropertyIncomeStatement, PropertyCategory
from properties.models import Property, Transactions
from .forms import PropertyIncomeStatementForm, PropertyCategoryForm
from copy import deepcopy


@login_required(login_url='/login/')
def incomestatement_property_list_view(request, year):
    property_list = request.GET.getlist("properties")
    prop_qs = Property.objects.filter(user=request.user)
    prop_cat = PropertyCategory.objects.filter(user=request.user)
    if not property_list:
        qs = PropertyIncomeStatement.objects.filter(user=request.user)
    else:
        qs = PropertyIncomeStatement.objects.filter(
            property__in=property_list, user=request.user
        ).order_by("-date")
    income_statement_list = PropertyIncomeStatement.objects.filter(user=request.user).order_by("-date")
    total_income = 0
    total_expense = 0
    total = 0
    for item in qs:
        cat_qs = PropertyCategory.objects.filter(user=request.user).get(name=item.propcategory)
        if cat_qs.transaction_type == "Income":
            total_income += item.amount
        else:
            total_expense += item.amount

    total = total_income - total_expense
    years = PropertyIncomeStatement.objects.filter(user=request.user).values_list("date__year").distinct()
    years_list = []
    for data in years:
        for item in data:
            years_list.append(item)
    years_list = sort_years_list(years_list)
    context = {
        "object_list": qs,
        "prop_qs": prop_qs,
        "income_statement_list": income_statement_list,
        "total": total,
        "prop_cat": prop_cat,
        "years_list": years_list,
    }
    return render(request, "propertyincomestatements/main.html", context)


def expense_budget_total(request, year):
    month_total = {
        1: {
            "name": "january_budget",
            "total": 0,
        },
        2: {
            "name": "february_budget",
            "total": 0,
        },
        3: {
            "name": "march_budget",
            "total": 0,
        },
        4: {
            "name": "april_budget",
            "total": 0,
        },
        5: {
            "name": "may_budget",
            "total": 0,
        },
        6: {
            "name": "june_budget",
            "total": 0,
        },
        7: {
            "name": "july_budget",
            "total": 0,
        },
        8: {
            "name": "august_budget",
            "total": 0,
        },
        9: {
            "name": "september_budget",
            "total": 0,
        },
        10: {
            "name": "october_budget",
            "total": 0,
        },
        11: {
            "name": "november_budget",
            "total": 0
        },
        12: {
            "name": "december_budget",
            "total": 0,
        },
    }
    for i in range(1, 13):
        data = PropertyCategory.objects.filter(transaction_type="Expense", user=request.user, year=year).values_list(
            month_total[i]["name"])
        total = 0
        for j in data:
            total += j[0]
        month_total[i]["total"] = total
    return month_total


def addcategory_incomestatements(request):
    print(request.body)
    if request.method == "POST":
        print(request.body, "property")
        categoryData = json.loads(request.body)
        obj = PropertyCategory.objects.create(
            name=categoryData['name'],
            transaction_type=categoryData["Transaction"],
            january_budget=categoryData["january_budget"],
            february_budget=categoryData['february_budget'],
            march_budget=categoryData['march_budget'],
            april_budget=categoryData['april_budget'],
            may_budget=categoryData['may_budget'],
            june_budget=categoryData['june_budget'],
            july_budget=categoryData['july_budget'],
            august_budget=categoryData['august_budget'],
            september_budget=categoryData['september_budget'],
            october_budget=categoryData['october_budget'],
            november_budget=categoryData['november_budget'],
            december_budget=categoryData['december_budget'],
            year=categoryData['year'],
            user=request.user
        )
        user = {
            'name': obj.name,
        }
        data = {
            'user': user
        }
        print(data, 'data')
        return JsonResponse(data)


def edit_category(request):
    if request.method == "POST":
        print(request.body, "property")
        propertyData = json.loads(request.body)
        property = PropertyCategory.objects.filter(user=request.user).get(id=propertyData['id'])
        property.name = propertyData['name']
        property.transaction_type = propertyData['transaction_type']
        property.january_budget = propertyData['january_budget']
        property.february_budget = propertyData['february_budget']
        property.march_budget = propertyData['march_budget']
        property.april_budget = propertyData['april_budget']
        property.may_budget = propertyData['may_budget']
        property.june_budget = propertyData['june_budget']
        property.july_budget = propertyData['july_budget']
        property.august_budget = propertyData['august_budget']
        property.september_budget = propertyData['september_budget']
        property.october_budget = propertyData['october_budget']
        property.november_budget = propertyData['november_budget']
        property.december_budget = propertyData['december_budget']
        property.year = propertyData['year']
        property.save()
        data = {
            'user': "data is updated"
        }
        return JsonResponse(data)


def delete_category(request):
    id1 = request.GET.get('id', None)
    print(id1, "delete")
    PropertyCategory.objects.filter(user=request.user).get(id=id1).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)


def income_budget_total(request, year):
    month_total = {
        1: {
            "name": "january_budget",
            "total": 0,
        },
        2: {
            "name": "february_budget",
            "total": 0,
        },
        3: {
            "name": "march_budget",
            "total": 0,
        },
        4: {
            "name": "april_budget",
            "total": 0,
        },
        5: {
            "name": "may_budget",
            "total": 0,
        },
        6: {
            "name": "june_budget",
            "total": 0,
        },
        7: {
            "name": "july_budget",
            "total": 0,
        },
        8: {
            "name": "august_budget",
            "total": 0,
        },
        9: {
            "name": "september_budget",
            "total": 0,
        },
        10: {
            "name": "october_budget",
            "total": 0,
        },
        11: {
            "name": "november_budget",
            "total": 0
        },
        12: {
            "name": "december_budget",
            "total": 0,
        },
    }
    yearly_income_budget = 0
    for i in range(1, 13):
        data = PropertyCategory.objects.filter(transaction_type="Income", user=request.user, year=year).values_list(
            month_total[i]["name"])
        total = 0
        for j in data:
            total += j[0]
        month_total[i]["total"] = total
    return month_total


def category_list(request, year):
    category_data = PropertyCategory.objects.filter(user=request.user, year=year)
    years = PropertyCategory.objects.filter(user=request.user).values_list("year").distinct()
    print(years, 'years')
    years_list = []
    for data in years:
        for item in data:
            years_list.append(int(item))
    years_list = sort_years_list(years_list)
    income_budget = income_budget_total(request, year)
    yearly_income_budget = 0
    for i in income_budget.values():
        yearly_income_budget += i["total"]
    expense_budget = expense_budget_total(request, year)
    yearly_expense_budget = 0
    for i in expense_budget.values():
        yearly_expense_budget += i["total"]
    context = {
        'category_list': category_data,
        "years_list": years_list,
        "income": income_budget_total(request, year),
        "expense": expense_budget_total(request, year),
        "yearly_income_budget": yearly_income_budget,
        "yearly_expense_budget": yearly_expense_budget,
        "current_year": year
    }
    return render(
        request, "incomestatements/category_property.html", context
    )


def addproperty_incomestatements(request):
    if request.method == "POST":
        print(request.body, "property")
        propertyData = json.loads(request.body)
        obj = PropertyIncomeStatement.objects.create(
            name=propertyData['name'],
            property=Property.objects.filter(user=request.user).get(name=propertyData["property"]),
            date=propertyData["date"],
            propcategory=PropertyCategory.objects.filter(user=request.user).get(name=propertyData["propcategory"]),
            amount=propertyData["amount"],
            user=request.user
        )
        user = {
            'name': obj.name,
        }
        data = {
            'user': user
        }
        print(data, 'data')
        return JsonResponse(data)


def editproperty_incomestatements(request):
    if request.method == "POST":
        print(request.body, "property")
        propertyData = json.loads(request.body)
        property = PropertyIncomeStatement.objects.filter(user=request.user).get(id=propertyData['id'])
        property.name = propertyData['name']
        property.property = Property.objects.filter(user=request.user).get(name=propertyData["property"])
        property.propcategory = PropertyCategory.objects.filter(user=request.user).get(
            name=propertyData["propcategory"])
        property.amount = propertyData['amount']
        property.save()
        data = {
            'user': "data is updated"
        }
        return JsonResponse(data)


def deleteproperty_incomestatement(request):
    id1 = request.GET.get('id', None)
    print(id1, "delete")
    PropertyIncomeStatement.objects.filter(user=request.user).get(id=id1).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)


def delete_property_incomestatement(request, pk):
    propertyincomestatement = PropertyIncomeStatement.objects.filter(user=request.user).get(id=pk)
    qs = PropertyIncomeStatement.objects.filter(user=request.user).get(id=pk)
    context = {
        "object": qs,
    }

    if request.method == "POST":
        propertyincomestatement.delete()
        return HttpResponse('<script type="text/javascript">window.close()</script>')

    return render(request, "propertyincomestatements/delete.html", context)


def sort_years_list(myList):
    myList.sort()
    return myList


def year_to_date(request, year):
    years = PropertyIncomeStatement.objects.filter(user=request.user).values_list("date__year").distinct()
    years_list = []
    for data in years:
        for item in data:
            years_list.append(item)
    years_list = sort_years_list(years_list)

    prop_qs = Property.objects.filter(user=request.user)
    property_list = request.GET.getlist("properties")
    if not property_list:
        qs = PropertyIncomeStatement.objects.filter(user=request.user)
    else:
        qs = PropertyIncomeStatement.objects.filter(
            property__in=property_list, user=request.user
        ).order_by("-date")

    qs = qs.filter(date__year=year)
    cat_dict = PropertyCategory.objects.filter(user=request.user)
    categories = {}

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
    total_expense = 0
    for month, amount in month_expenses.items():
        total_expense += amount
    month_expenses.update({"total": total_expense})

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
    total_income = 0
    for month, amount in month_income.items():
        total_income += amount
    month_income.update({"total": total_income})

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
    income_result = {}
    unique_categories_of_income = income_qs.values("propcategory__name").distinct()
    for category in unique_categories_of_income:
        income_result[f"{list(category.values())[0]}"] = {
            "months": deepcopy(monthly_income_data),
            "total": 0,
        }

    for month in monthly_income_data.keys():
        current_month_total_income = 0
        month_int = datetime.datetime.strptime(month, "%B").month
        current_month_income = income_qs.filter(date__month=month_int)
        for income_in_current_month in current_month_income:
            current_month_total_income += income_in_current_month.amount
            category_of_income = PropertyCategory.objects.filter(user=request.user).get(
                name=income_in_current_month.propcategory
            )
            income_result[f"{category_of_income}"]["months"][f"{month}"] = float(
                current_month_total_income
            )

    for category in unique_categories_of_income:
        income_result[f"{list(category.values())[0]}"]["total"] = sum(
            income_result[f"{list(category.values())[0]}"]["months"].values()
        )
    print("income_result", income_result)
    # #### END OF CATEGORIES EACH MONTH TOTAL INCOME ####

    # START OF CATEGORIES EACH MONTH TOTAL EXPENSES
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
    unique_categories_of_expenses = expense_qs.values("propcategory__name").distinct()
    expenses_result = {}
    for category in unique_categories_of_expenses:
        expenses_result[f"{list(category.values())[0]}"] = {
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
            category_of_expense = PropertyCategory.objects.filter(user=request.user).get(
                name=expense_in_current_month.propcategory
            )
            expenses_result[f"{category_of_expense}"]["months"][f"{month}"] = float(
                current_month_total_expense
            )

    for category in unique_categories_of_expenses:
        expenses_result[f"{list(category.values())[0]}"]["total"] = sum(
            expenses_result[f"{list(category.values())[0]}"]["months"].values()
        )
    #  #### END OF CATEGORIES EACH MONTH TOTAL EXPENSES ####

    # Yearly Sum of each category expense
    categories_total_yearly = {}
    for item in cat_dict:
        categories_total_yearly[item.name] = 0
        categories[item.name] = 0
    for item in expense_qs:
        cat_qs = PropertyCategory.objects.filter(user=request.user).get(name=item.propcategory)
        if cat_qs.name in categories_total_yearly:
            categories_total_yearly[cat_qs.name] += item.amount

    total_income = 0
    total_expense = 0
    for item in qs:
        cat_qs = PropertyCategory.objects.filter(user=request.user).get(name=item.propcategory)
        if cat_qs.transaction_type == "Income":
            total_income += item.amount
        else:
            total_expense += item.amount

    total = total_income - total_expense
    category_total_yearly = {x: y for x, y in categories_total_yearly.items() if y != 0}
    net_income = []
    for key, value in month_expenses.items():
        net_income.append(month_income[key] - month_expenses[key])
    print(net_income, 'ki bnaya a')
    context = {
        "object_list": qs,
        "year": year,
        "total": total,
        "income": total_income,
        "expense": total_expense,
        "categories_yearly": category_total_yearly,
        "month_expenses": month_expenses,
        "month_income": month_income,
        "net_income": net_income,
        "prop_qs": prop_qs,
        "years_list": years_list,
        "expenses_result": expenses_result,
        "income_result": income_result,
    }
    return render(request, "propertyincomestatements/ytd.html", context)
