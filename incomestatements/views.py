import datetime
import json
from copy import deepcopy

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader

from incomestatements_property.views import sort_years_list
from .models import IncomeStatement, Category, CategoryName
from .forms import IncomeStatementForm, CategoryForm
from django.db.models.functions import TruncMonth, ExtractMonth
from django.db.models import Count, Sum, FloatField


@login_required(login_url='/login/')
def incomestatements_list_view(request, year):
    prop_cat = Category.objects.filter(user=request.user, year=year)
    if request.method == "POST":
        form = IncomeStatementForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "incomestatements/main.html")
    else:
        qs = IncomeStatement.objects.filter(user=request.user, date__year=year)
        total_income = 0
        total_expense = 0
        total = 0
        for item in qs:
            cat_qs = Category.objects.filter(user=request.user, year=year).get(name=item.category)
            if cat_qs.transaction_type == "Income":
                total_income += item.amount
            else:
                total_expense += item.amount

        total = total_income - total_expense
        years = IncomeStatement.objects.filter(user=request.user).values_list("date__year").distinct()
        years_list = []
        for data in years:
            for item in data:
                years_list.append(item)
        years_list = sort_years_list(years_list)
        context = {
            "year": year,
            "object_list": qs,
            "total": total,
            "prop_cat": prop_cat,
            "years_list": years_list,
        }
        return render(request, "incomestatements/main.html", context)


def addcategory_incomestatements(request):
    if request.method == "POST":
        print(request.body, "property")
        categoryData = json.loads(request.body)
        obj = Category.objects.create(
            name=categoryData['name'],
            transaction_type=categoryData["Transaction"],
            year=categoryData["year"],
            january_budget=categoryData['january_budget'],
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

def addcategory2_incomestatements(request):
    if request.method == "POST":
        print(request.body, "property")
        categoryData = json.loads(request.body)
        obj = Category.objects.create(
            name=categoryData['name'],
            transaction_type=categoryData["Transaction"],
            year=categoryData["year"],
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

def addproperty_incomestatements(request):
    if request.method == "POST":
        print(request.body, "property")
        propertyData = json.loads(request.body)
        obj = IncomeStatement.objects.create(
            name=propertyData['name'],
            date=propertyData["date"],
            category=Category.objects.filter(user=request.user).get(name=propertyData["propcategory"]),
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
        property = IncomeStatement.objects.filter(user=request.user).get(id=propertyData['id'])
        property.name = propertyData['name']
        property.propcategory = Category.objects.filter(user=request.user).get(name=propertyData["propcategory"])
        property.amount = propertyData['amount']
        property.save()
        data = {
            'user': "data is updated"
        }
        return JsonResponse(data)


def edit_category(request):
    if request.method == "POST":
        print(request.body, "property")
        propertyData = json.loads(request.body)
        property = Category.objects.filter(user=request.user).get(id=propertyData['id'])
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
    Category.objects.filter(user=request.user).get(id=id1).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)


def show_report(request, category, year):
    category_data = Category.objects.filter(user=request.user).get(name=category)
    monthly = category_data.months_data()
    if category_data.transaction_type == 'Income':
        report_data = incomes_result(request, year, category)
    else:
        report_data = expense_result(request, year, category)
    monthly_data = {
        1: {
            "name": "January",
            "budget": 0,
            "actual": 0,
            "difference": 0,
            "percentage": 0,
        },
        2: {
            "name": "February",
            "budget": 0,
            "actual": 0,
            "difference": 0,
            "percentage": 0,
        },
        3: {
            "name": "March",
            "budget": 0,
            "actual": 0,
            "difference": 0,
            "percentage": 0,
        },
        4: {
            "name": "April",
            "budget": 0,
            "actual": 0,
            "difference": 0,
            "percentage": 0,
        },
        5: {
            "name": "May",
            "budget": 0,
            "actual": 0,
            "difference": 0,
            "percentage": 0,
        },
        6: {
            "name": "June",
            "budget": 0,
            "actual": 0,
            "difference": 0,
            "percentage": 0,
        },
        7: {
            "name": "July",
            "budget": 0,
            "actual": 0,
            "difference": 0,
            "percentage": 0,
        },
        8: {
            "name": "August",
            "budget": 0,
            "actual": 0,
            "difference": 0,
            "percentage": 0,
        },
        9: {
            "name": "September",
            "budget": 0,
            "actual": 0,
            "difference": 0,
            "percentage": 0,
        },
        10: {
            "name": "October",
            "budget": 0,
            "actual": 0,
            "difference": 0,
            "percentage": 0,
        },
        11: {
            "name": "November",
            "budget": 0,
            "actual": 0,
            "difference": 0,
            "percentage": 0,
        },
        12: {
            "name": "December",
            "budget": 0,
            "actual": 0,
            "difference": 0,
            "percentage": 0,
        },
    }
    summary = []
    for x in range(1, 13):
        monthly_data[x]['budget'] = monthly[monthly_data[x]['name']]
        monthly_data[x]['actual'] = report_data[category]['months'][monthly_data[x]['name']]
        monthly_data[x]['difference'] = monthly_data[x]['budget'] - monthly_data[x]['actual']
        if monthly_data[x]['budget'] != 0 and monthly_data[x]['actual'] != 0:
            monthly_data[x]['percentage'] = float(
                "{:.1f}".format(monthly_data[x]['actual'] / monthly_data[x]['budget'] * 100))
        else:
            monthly_data[x]['percentage'] = 0
        summary.append(monthly_data[x])

    print(summary, 'x')
    percentage = float("{:.1f}".format(report_data[category]['total'] / category_data.compute_budget() * 100))
    context = {
        "transaction_type": category_data.transaction_type,
        "year": year,
        "category_name": category_data.name,
        "budget": category_data,
        "report_data": report_data[category],
        "percentage": percentage,
        "summary": monthly_data,
    }
    return render(
        request, "incomestatements/report.html", context
    )


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
        data = Category.objects.filter(transaction_type="Expense", user=request.user, year=year).values_list(
            month_total[i]["name"])
        total = 0
        for j in data:
            total += j[0]
        month_total[i]["total"] = total
    return month_total


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
        data = Category.objects.filter(transaction_type="Income", user=request.user, year=year).values_list(
            month_total[i]["name"])
        total = 0
        for j in data:
            total += j[0]
        month_total[i]["total"] = total
    return month_total


def category_list(request, year):
    category_data = Category.objects.filter(user=request.user, year=year)
    category_name = CategoryName.objects.filter(user=request.user)
    years = Category.objects.filter(user=request.user).values_list("year").distinct()
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
        "category_name": category_name,
        'category_list': category_data,
        "years_list": years_list,
        "income": income_budget_total(request, year),
        "expense": expense_budget_total(request, year),
        "yearly_income_budget": yearly_income_budget,
        "yearly_expense_budget": yearly_expense_budget,
        "current_year": year
    }
    return render(
        request, "incomestatements/category.html", context
    )


def deleteproperty_incomestatement(request):
    id1 = request.GET.get('id', None)
    print(id1, "delete")
    IncomeStatement.objects.filter(user=request.user).get(id=id1).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)


def add_incomestatements(request, year):
    if request.method == "POST":
        form = IncomeStatementForm(request.user, year, request.POST)
        if form.is_valid():
            incomestatement = form.save(commit=False)
            incomestatement.user = request.user
            incomestatement.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "transactionListChanged": None,
                        "showMessage": f"{incomestatement.name} added."
                    })
                })
    else:
        form = IncomeStatementForm(request.user, year)
    return render(request, "incomestatements/add.html", {"form": form})


def data_list(request, year=''):
    if year == '':
        prop_cat = Category.objects.filter(user=request.user)
    else:
        prop_cat = Category.objects.filter(user=request.user, year=year)
    if request.method == "POST":
        form = IncomeStatementForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "incomestatements/main.html")
    else:
        qs = IncomeStatement.objects.filter(user=request.user, date__year=year)
        total_income = 0
        total_expense = 0
        total = 0
        for item in qs:
            cat_qs = Category.objects.filter(user=request.user, year=year).get(name=item.category.name)
            if cat_qs.transaction_type == "Income":
                total_income += item.amount
            else:
                total_expense += item.amount

        total = total_income - total_expense
        years = IncomeStatement.objects.filter(user=request.user).values_list("date__year").distinct()
        years_list = []
        for data in years:
            for item in data:
                years_list.append(item)
        years_list = sort_years_list(years_list)
        context = {
            "year": year,
            "object_list": qs,
            "total": total,
            "prop_cat": prop_cat,
            "years_list": years_list,
        }
        return render(request, "incomestatements/data_list.html", context)


def update_incomestatements(request, pk, year):
    incomestatement = get_object_or_404(IncomeStatement, pk=pk)
    if request.method == "POST":
        form = IncomeStatementForm(request.user, year, request.POST, instance=incomestatement)
        if form.is_valid():
            incomestatement = form.save(commit=False)
            incomestatement.user = request.user
            incomestatement.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "transactionListChanged": None,
                        "showMessage": f"{incomestatement.name} updated."
                    })
                }
            )
    else:
        form = IncomeStatementForm(request.user, year, instance=incomestatement)
    return render(request, 'incomestatements/add.html', {
        'form': form,
        'incomestatement': incomestatement,
    })


def delete_incomestatement(request, pk):
    incomestatement = IncomeStatement.objects.filter(user=request.user).get(id=pk)
    qs = IncomeStatement.objects.filter(user=request.user).get(id=pk)
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
    category = Category.objects.filter(user=request.user).get(id=pk)
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


def incomes_result(request, year, category):
    qs = IncomeStatement.objects.filter(date__year=year, user=request.user)
    income_qs = qs.filter(category__transaction_type="Income", category__name=category)
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
    for category in unique_categories_of_income:
        for month in monthly_income_data.keys():
            current_month_total_income = 0
            month_int = datetime.datetime.strptime(month, "%B").month
            current_month_income = income_qs.filter(date__month=month_int, category__name=category['category__name'])
            # print(month, current_month_income)
            for income_in_current_month in current_month_income:
                current_month_total_income += income_in_current_month.amount
                category_of_income = Category.objects.filter(user=request.user, year=year).get(
                    name=income_in_current_month.category
                )
                income_result[f"{category_of_income}"]["months"][f"{month}"] = float(
                    current_month_total_income
                )
    total_income_budget = 0
    for category in unique_categories_of_income:
        income_result[f"{list(category.values())[0]}"]["total"] = sum(
            income_result[f"{list(category.values())[0]}"]["months"].values()
        )
        budget_category = Category.objects.filter(user=request.user, year=year).get(name=category['category__name'])
        income_result[f"{list(category.values())[0]}"]["Budget"] = budget_category.compute_budget()
        total_income_budget += budget_category.compute_budget()
        category_total = income_result[f"{list(category.values())[0]}"]["total"]
        category_budget = income_result[f"{list(category.values())[0]}"]["Budget"]
        percentage = float(category_total) / float(category_budget) * 100
        income_result[f"{list(category.values())[0]}"]["percentage"] = percentage
        print(percentage, 'percentage')
    # #### END OF CATEGORIES EACH MONTH TOTAL Income ####
    return income_result


def expense_result(request, year, category):
    qs = IncomeStatement.objects.filter(date__year=year, user=request.user)
    expense_qs = qs.filter(category__transaction_type="Expense", category__name=category)
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

    for category_expense in unique_categories_of_expenses:
        for month in monthly_expenses_data.keys():
            current_month_total_expense = 0
            month_int = datetime.datetime.strptime(month, "%B").month
            current_month_expenses = expense_qs.filter(date__month=month_int,
                                                       category__name=category_expense['category__name'])
            # print(month, current_month_expenses)
            for expense_in_current_month in current_month_expenses:
                current_month_total_expense += expense_in_current_month.amount
                category_of_expense = Category.objects.filter(user=request.user).get(
                    name=expense_in_current_month.category
                )
                expenses_result[f"{category_of_expense}"]["months"][f"{month}"] = float(
                    current_month_total_expense
                )
    total_expense_budget = 0
    for category_expense in unique_categories_of_expenses:
        expenses_result[f"{list(category_expense.values())[0]}"]["total"] = sum(
            expenses_result[f"{list(category_expense.values())[0]}"]["months"].values()
        )
        budget_category = Category.objects.filter(user=request.user, year=year).get(
            name=category_expense['category__name'])
        expenses_result[f"{list(category_expense.values())[0]}"]["Budget"] = budget_category.compute_budget()
        total_expense_budget += Category.objects.filter(user=request.user, year=year).get(
            name=category_expense['category__name']
        ).compute_budget()
        category_total = expenses_result[f"{list(category_expense.values())[0]}"]["total"]
        category_budget = expenses_result[f"{list(category_expense.values())[0]}"]["Budget"]
        percentage = float(category_total) / float(category_budget) * 100
        expenses_result[f"{list(category_expense.values())[0]}"]["percentage"] = percentage
    #### END OF CATEGORIES EACH MONTH TOTAL EXPENSES ####
    return expenses_result


def year_to_date(request, year):
    qs = IncomeStatement.objects.filter(date__year=year, user=request.user)
    cat_dict = Category.objects.filter(user=request.user, year=year)
    expense_qs = qs.filter(category__transaction_type="Expense")
    income_qs = qs.filter(category__transaction_type="Income")
    categories_income_yearly = {}
    for item in cat_dict:
        categories_income_yearly[item.name] = 0
    for item in income_qs:
        cat_qs = Category.objects.filter(user=request.user, year=year).get(name=item.category)
        if cat_qs.name in categories_income_yearly:
            categories_income_yearly[cat_qs.name] += item.amount
        else:
            print("Here is thing")
    categories_income_yearly = {
        x: y for x, y in categories_income_yearly.items() if y != 0
    }
    categories_expense_yearly = {}
    for item in cat_dict:
        categories_expense_yearly[item.name] = 0
    for item in expense_qs:
        cat_qs = Category.objects.filter(user=request.user, year=year).get(name=item.category)
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
        cat_qs = Category.objects.filter(user=request.user, year=year).get(name=item.category)
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
    print(month_expenses, 'total')
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
    for category in unique_categories_of_income:
        for month in monthly_income_data.keys():
            current_month_total_income = 0
            month_int = datetime.datetime.strptime(month, "%B").month
            current_month_income = income_qs.filter(date__month=month_int, category__name=category['category__name'])
            # print(month, current_month_income)
            for income_in_current_month in current_month_income:
                current_month_total_income += income_in_current_month.amount
                category_of_income = Category.objects.filter(user=request.user, year=year).get(
                    name=income_in_current_month.category
                )
                income_result[f"{category_of_income}"]["months"][f"{month}"] = float(
                    current_month_total_income
                )
    total_income_budget = 0
    if unique_categories_of_income:
        for category in unique_categories_of_income:
            income_result[f"{list(category.values())[0]}"]["total"] = sum(
                income_result[f"{list(category.values())[0]}"]["months"].values()
            )
            budget_category = Category.objects.filter(user=request.user, year=year).get(name=category['category__name'])
            income_result[f"{list(category.values())[0]}"]["Budget"] = budget_category.compute_budget()
            total_income_budget += budget_category.compute_budget()
            category_total = income_result[f"{list(category.values())[0]}"]["total"]
            category_budget = income_result[f"{list(category.values())[0]}"]["Budget"]
            percentage = float(category_total) / float(category_budget) * 100
            income_result[f"{list(category.values())[0]}"]["percentage"] = percentage
            print(percentage, 'percentage')
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

    for category_expense in unique_categories_of_expenses:
        for month in monthly_expenses_data.keys():
            current_month_total_expense = 0
            month_int = datetime.datetime.strptime(month, "%B").month
            current_month_expenses = expense_qs.filter(date__month=month_int,
                                                       category__name=category_expense['category__name'])
            # print(month, current_month_expenses)
            for expense_in_current_month in current_month_expenses:
                current_month_total_expense += expense_in_current_month.amount
                category_of_expense = Category.objects.filter(user=request.user, year=year).get(
                    name=expense_in_current_month.category
                )
                expenses_result[f"{category_of_expense}"]["months"][f"{month}"] = float(
                    current_month_total_expense
                )
    total_expense_budget = 0
    for category_expense in unique_categories_of_expenses:
        expenses_result[f"{list(category_expense.values())[0]}"]["total"] = sum(
            expenses_result[f"{list(category_expense.values())[0]}"]["months"].values()
        )
        budget_category = Category.objects.filter(user=request.user, year=year).get(
            name=category_expense['category__name'], year=year)
        expenses_result[f"{list(category_expense.values())[0]}"]["Budget"] = budget_category.compute_budget()
        total_expense_budget += Category.objects.filter(user=request.user, year=year).get(
            name=category_expense['category__name'],
            year=year).compute_budget()
        category_total = expenses_result[f"{list(category_expense.values())[0]}"]["total"]
        category_budget = expenses_result[f"{list(category_expense.values())[0]}"]["Budget"]
        percentage = float(category_total) / float(category_budget) * 100
        expenses_result[f"{list(category_expense.values())[0]}"]["percentage"] = percentage
        print(percentage, 'percentage')
    #  #### END OF CATEGORIES EACH MONTH TOTAL EXPENSES ####

    years = list(IncomeStatement.objects.filter(user=request.user).values_list("date__year").distinct())
    years_list = []
    for each in years:
        for item in each:
            years_list.append(item)
    years_list = sort(years_list)
    print(month_income, 'month_income')
    print(month_expenses, 'month_expenses')
    # income_result['test'].update({"Budget": 10000})
    month_income.update({"Budget": total_income_budget})
    month_expenses.update({"Budget": total_expense_budget})
    net_income = []
    for key, value in month_expenses.items():
        net_income.append(month_income[key] - month_expenses[key])
    print(total_expense, 'total_expense_print')
    print(total_expense_budget, 'total_expense_budget_print')
    net_total = month_income["total"] - month_expenses["total"]
    net_Budget = month_income["Budget"] - month_expenses["Budget"]
    print(net_total, net_Budget)
    if total_income != 0 and total_income_budget != 0:
        income_budget_percentage = (float(total_income) / float(total_income_budget)) * 100
    else:
        income_budget_percentage = 0
    if total_expense != 0 and total_expense_budget != 0:
        expense_budget_percentage = (float(total_expense) / float(total_expense_budget)) * 100,
    else:
        expense_budget_percentage = 0
    context = {
        "object_list": qs,
        "year": year,
        "total_income": total_income,
        "income_budget": total_income_budget,
        "total_expense": total_expense,
        "expense_budget": total_expense_budget,
        "total_amount": net_amount,
        "month_expenses": month_expenses,
        "month_income": month_income,
        "categories_expense_yearly": categories_expense_yearly,
        "categories_income_yearly": categories_income_yearly,
        "years_list": years_list,
        "income_result": income_result,
        "expenses_result": expenses_result,
        "net_income": net_income,
        "income_budget_percentage": income_budget_percentage,
        "expense_budget_percentage": expense_budget_percentage,
        # "total_budget_percentage": (float(net_total) / float(net_Budget)) * 100
    }
    return render(request, "incomestatements/ytd.html", context)
