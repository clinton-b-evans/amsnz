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
    for item in qs:
        cat_qs = PropertyCategory.objects.get(name=item.propcategory)
        if cat_qs.transaction_type == "Income":
            total_income += item.amount
        else:
            total_expense += item.amount
    total = total_income - total_expense
    categories = {x: y for x, y in categories.items() if y != 0}

    # expense_name = ''
    # expense_date_time = ''
    # expense_prop_name = ''
    # for key in categories:
    #     qs_prop_is = PropertyIncomeStatement.objects.get(propcategory__name=key, date__year=year)
    #     expense_name += qs_prop_is.name
    #     expense_date = qs_prop_is.date
    #     expense_date_time = expense_date
    #     expense_prop_name += qs_prop_is.property.name
    # print(expense_date_time)
    # print(expense_name)
    # print(expense_prop_name)
    context = {
        "object_list": qs,
        "year": year,
        "total": total,
        "income": total_income,
        "expense": total_expense,
        "categories": categories,
        "prop_qs": prop_qs,
    }
    return render(request, "propertyincomestatements/ytd.html", context)


# def expense_category_detail_view(request, **kwargs):
#     name = kwargs.get("name")
#     props_income_qs = PropertyIncomeStatement.objects.all()
#     qs = props_income_qs.filter(propcategory=name)
#     props_list = []
#     for item in qs:
#         props_list[item.name] += item.name
#         props_list[item.amount] += item.amount
#         props_list[item.property.name] += item.property.name
#         props_list[item.date] += item.date
#
#     print(props_list)
#     return HttpResponse(props_list)
