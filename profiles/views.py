from django.shortcuts import render
from .models import Property
from django.db.models import Sum
from datetime import date


# Create your views here.


def home_view(request):
    return render(request, "properties/home.html", {})


def property_list_view(request):
    qs = Property.objects.all()
    total_market_value = qs.aggregate(Sum("market_value")).get("market_value__sum")
    total_loan_amount = qs.aggregate(Sum("loan_amount")).get("loan_amount__sum")
    total_rent = Property.objects.all().aggregate(Sum("rent")).get("rent__sum")
    total_rent = f"{total_rent:,}"
    context = {
        "object_list": qs,
        "total_market_value": total_market_value,
        "total_loan_amount": total_loan_amount,
        "total_rent": total_rent,
    }
    return render(request, "properties/main.html", context)


def property_detail_view(request, **kwargs):
    pk = kwargs.get("pk")
    obj = Property.objects.get(pk=pk)
    loan_term_left = obj.loan_term - (date.today().year - obj.purchase_date.year)
    equity = obj.market_value - obj.loan_amount

    rent_monthly = obj.rent / 12
    rent_weekly = obj.rent / 52

    rent_after_vacany_rate = obj.rent - (obj.rent * (obj.vacancy_rate / 100))
    rent_after_vancany_rate_weekly = rent_after_vacany_rate / 52
    rent_after_vacany_rate_monthly = rent_after_vacany_rate / 12

    operating_expenses = (
        obj.insurance + obj.management_fee + obj.maintenance + obj.rates
    )
    operating_expenses_monthly = operating_expenses / 12
    operating_expenses_weekly = operating_expenses / 52

    net_operating_income = rent_after_vacany_rate - operating_expenses
    net_operating_income_monthly = net_operating_income / 12
    net_operating_income_weekly = net_operating_income / 52
    net_operating_income_percent = (net_operating_income / rent_after_vacany_rate) * 100

    cap_rate = (net_operating_income / obj.market_value) * 100
    gross_yield = (rent_after_vacany_rate / obj.market_value) * 100
    loan_to_value = (obj.loan_amount / obj.market_value) * 100
    mortgage_repayment = obj.repayments
    mortgage_repayment_monthly = obj.repayments / 12
    mortgage_repayment_weekly = obj.repayments / 52

    net_income = net_operating_income - mortgage_repayment
    net_income_monthly = net_income / 12
    net_income_weekly = net_income / 52

    context = {
        "object": obj,
        "loan_term_left": loan_term_left,
        "equity": equity,
        "rent_monthly": rent_monthly,
        "rent_weekly": rent_weekly,
        "rent_after_vacany_rate": rent_after_vacany_rate,
        "rent_after_vancany_rate_weekly": rent_after_vancany_rate_weekly,
        "rent_after_vacany_rate_monthly": rent_after_vacany_rate_monthly,
        "operating_expenses": operating_expenses,
        "operating_expenses_weekly": operating_expenses_weekly,
        "operating_expenses_monthly": operating_expenses_monthly,
        "net_operating_income": net_operating_income,
        "net_operating_income_monthly": net_operating_income_monthly,
        "net_operating_income_weekly": net_operating_income_weekly,
        "net_operating_income_percent": net_operating_income_percent,
        "cap_rate": cap_rate,
        "gross_yield": gross_yield,
        "loan_to_value": loan_to_value,
        "mortgage_repayment": mortgage_repayment,
        "mortgage_repayment_monthly": mortgage_repayment_monthly,
        "mortgage_repayment_weekly": mortgage_repayment_weekly,
        "net_income": net_income,
        "net_income_monthly": net_income_monthly,
        "net_income_weekly": net_income_weekly,
    }
    return render(request, "properties/detail.html", context)


def property_summary_view(request):
    qs = Property.objects.all()
    total_properties = qs.count()
    total_assets = qs.aggregate(Sum("market_value")).get("market_value__sum")
    total_liabilities = qs.aggregate(Sum("loan_amount")).get("loan_amount__sum")
    total_rent = qs.aggregate(Sum("rent")).get("rent__sum")
    total_other_income = qs.aggregate(Sum("other_income")).get("other_income__sum")

    total_insurance = qs.aggregate(Sum("insurance")).get("insurance__sum")
    total_management_fee = qs.aggregate(Sum("management_fee")).get(
        "management_fee__sum"
    )
    total_maintenance = qs.aggregate(Sum("maintenance")).get("maintenance__sum")
    total_rates = qs.aggregate(Sum("rates")).get("rates__sum")
    total_repayments = qs.aggregate(Sum("repayments")).get("repayments__sum")

    if total_insurance == None:
        total_insurance = 0

    if total_management_fee == None:
        total_management_fee = 0

    if total_maintenance == None:
        total_maintenance = 0

    if total_rates == None:
        total_rates = 0

    if total_other_income == None:
        total_other_income = 0
    total_income = total_rent + total_other_income
    total_networth = total_assets - total_liabilities

    total_operating_expenses = (
        total_insurance + total_management_fee + total_maintenance + total_rates
    )
    total_expenses = total_operating_expenses + total_repayments

    total_net_rental_income = total_income - total_expenses

    context = {
        "object_list": qs,
        "total_properties": total_properties,
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "total_networth": total_networth,
        "total_income": total_income,
        "total_rent": total_rent,
        "total_other_income": total_other_income,
        "total_operating_expenses": total_operating_expenses,
        "total_repayments": total_repayments,
        "total_expenses": total_expenses,
        "total_net_rental_income": total_net_rental_income,
        "net_income": net_income,
        "net_income_monthly": net_income_monthly,
        "net_income_weekly": net_income_weekly,
    }
    return render(request, "properties/summary.html", context)
