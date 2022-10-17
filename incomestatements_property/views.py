from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from incomestatements.forms import CategoryForm
from incomestatements.models import Category
from .models import PropertyIncomeStatement, PropertyCategory
from properties.models import Property, Transactions
from .forms import PropertyIncomeStatementForm, PropertyCategoryForm


def incomestatement_property_list_view(request):
    property_list = request.GET.getlist("properties")
    prop_qs = Property.objects.all()
    qs = PropertyIncomeStatement.objects.filter(property__in=property_list).order_by(
        "-date"
    )
    print(qs)
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


"""
function to display yearly profit and loss
"""


def year_to_date(request, year):
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
    for item in cat_dict:
        categories[item.name] = 0
        # categories[item.property] = ''

    for item in qs:
        cat_qs = PropertyCategory.objects.get(name=item.propcategory)
        # categories[item.property] += item.property.name

        if cat_qs.name in categories:
            categories[cat_qs.name] += item.amount

        else:
            print("Here is thing")
    print("#### category Data #####", categories)
    total_income = 0
    total_expense = 0
    total = 0
    # get property category data by property name
    for item in qs:
        cat_qs = PropertyCategory.objects.get(name=item.propcategory)
        if cat_qs.transaction_type == "Income":
            total_income += item.amount
        else:
            total_expense += item.amount
    total = total_income - total_expense
    categories = {x: y for x, y in categories.items() if y != 0}
    # Active Categories
    print("Active Categories--->", categories)
    """
    extracted all Years from Database 
    """
    years = list(PropertyIncomeStatement.objects.values_list("date__year").distinct())
    years_list = []
    for data in years:
        for item in data:
            years_list.append(item)
    """
    Sort extracted Years
    """

    def sort(myList):
        myList.sort(reverse=True)
        return myList

    years_list = sort(years_list)
    context = {
        "object_list": qs,
        "year": year,
        "total": total,
        "income": total_income,
        "expense": total_expense,
        "categories": categories,
        "prop_qs": prop_qs,
        "years_list": years_list,
    }
    return render(request, "propertyincomestatements/ytd.html", context)
