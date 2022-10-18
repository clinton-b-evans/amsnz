from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import IncomeStatement, Category
from .forms import IncomeStatementForm, CategoryForm


# Create your views here.
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


def year_to_date(request, year):
    qs = IncomeStatement.objects.filter(date__year=year)
    cat_dict = Category.objects.all()
    categories = {}
    for item in cat_dict:
        categories[item.name] = 0
    for item in qs:
        cat_qs = Category.objects.get(name=item.category)
        print(cat_qs.name)
        print(item.amount)
        if cat_qs.name in categories:
            categories[cat_qs.name] += item.amount
        else:
            print("Here is thing")
    print(categories)
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

    categories = {x: y for x, y in categories.items() if y != 0}
    """
    extracted all Years from Database 
    """
    years = list(IncomeStatement.objects.values_list("date__year").distinct())
    years_list = []
    for data in years:
        for item in data:
            years_list.append(item)
    """
    Sort extracted Years List
    """

    def sort(myList):
        myList.sort(reverse=True)
        return myList

    years_list = sort(years_list)
    context = {
        "object_list": qs,
        "year": year,
        "total_income": total_income,
        "total_expense": total_expense,
        "total_amount": net_amount,
        "categories": categories,
        "years_list": years_list,
    }
    return render(request, "incomestatements/ytd.html", context)
