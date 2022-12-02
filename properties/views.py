import json
from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.utils.timezone import now
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect, JsonResponse,
)
from .forms import PropertyForm
from .models import Property, Transactions
from retirement_goals.models import RetirementGoal
from personal_balances.models import PersonalBalance
from commodities.models import Commodity, Transaction
from crypto.models import Crypto
from market_funds.models import IndexFund
from contacts.models import Contact
from reminders.models import Reminder
from cash_flows.models import CashFlow
from personal_balances.models import PersonalBalance
from django.db.models import Sum
from datetime import date, datetime
import numpy as np
import numpy_financial as npf


def home_view(request):
    return render(request, "properties/home.html", {})


@login_required(login_url='/login/')
def property_list_view(request):
    selected = "Yearly"
    qs = Property.objects.filter(user=request.user)
    print(qs, 'qs')
    total_operating_costs = 0
    total_noi = 0
    total_rent = 0
    for obj in qs:
        obj.rent_after_vacany_rate = obj.rent - (obj.rent * (obj.vacancy_rate / 100))
        obj.net_management = obj.rent_after_vacany_rate * (obj.management_fee / 100)
        obj.operating_cost = (
                obj.net_management
                + obj.insurance
                + obj.maintenance
                + obj.rates
                + obj.bodycorp_fee
        )
        total_operating_costs += obj.operating_cost
        obj.net_operating_income = obj.rent_after_vacany_rate - obj.operating_cost
        obj.cap_rate = obj.net_operating_income / obj.market_value * 100
        obj.loan_to_value = int(obj.loan_amount) / int(obj.market_value) * 100
        total_noi = total_noi + obj.net_operating_income
        obj.rent = obj.rent_after_vacany_rate
        total_rent = total_rent + obj.rent

    total_market_value = qs.aggregate(Sum("market_value")).get("market_value__sum")
    total_loan_amount = qs.aggregate(Sum("loan_amount")).get("loan_amount__sum")
    total_repayments = (
        Property.objects.filter(user=request.user).aggregate(Sum("repayments")).get("repayments__sum")
    )

    total_rates = Property.objects.filter(user=request.user).aggregate(Sum("rates")).get("rates__sum")
    total_insurance = (
        Property.objects.filter(user=request.user).aggregate(Sum("insurance")).get("insurance__sum")
    )
    total_maintenance = (
        Property.objects.filter(user=request.user).aggregate(Sum("maintenance")).get("maintenance__sum")
    )
    total_management_fee = (
        Property.objects.filter(user=request.user)
        .aggregate(Sum("management_fee"))
        .get("management_fee__sum")
    )
    if total_market_value:
        total_cap_rate = ((total_rent - total_operating_costs) / total_market_value) * 100
        total_loan_to_value = total_loan_amount / total_market_value * 100
    else:
        total_cap_rate = 0
        total_loan_to_value = 0
    context = {
        "object_list": qs,
        "total_market_value": total_market_value,
        "total_loan_amount": total_loan_amount,
        "total_loan_to_value": total_loan_to_value,
        "total_repayments": total_repayments,
        "total_rent": total_rent,
        "total_operating_costs": total_operating_costs,
        "total_cap_rate": total_cap_rate,
        "total_noi": total_noi,
        "selected": selected,
    }
    return render(request, "properties/main.html", context)


def property_list_weekly(request):
    selected = "Weekly"
    qs = Property.objects.filter(user=request.user)
    total_operating_costs = 0
    total_noi = 0
    total_rent = 0
    for obj in qs:
        obj.rent_after_vacany_rate = obj.rent - (obj.rent * (obj.vacancy_rate / 100))
        obj.net_management = obj.rent_after_vacany_rate * (obj.management_fee / 100)
        obj.operating_cost = (
                obj.net_management
                + obj.insurance
                + obj.maintenance
                + obj.rates
                + obj.bodycorp_fee
        )
        obj.operating_cost = obj.operating_cost / 52
        obj.net_operating_income = obj.rent_after_vacany_rate - obj.operating_cost * 52
        obj.cap_rate = obj.net_operating_income / obj.market_value * 100
        obj.net_operating_income = obj.net_operating_income / 52
        obj.loan_to_value = int(obj.loan_amount) / int(obj.market_value) * 100
        obj.rent = obj.rent_after_vacany_rate / 52
        obj.repayments = round(obj.repayments / 52, 2)
        total_noi = total_noi + obj.net_operating_income
        total_operating_costs += obj.operating_cost
        total_rent = total_rent + obj.rent

    total_market_value = qs.aggregate(Sum("market_value")).get("market_value__sum")
    total_loan_amount = qs.aggregate(Sum("loan_amount")).get("loan_amount__sum")
    total_repayments = (
        Property.objects.filter(user=request.user).aggregate(Sum("repayments")).get("repayments__sum")
    )

    total_rates = Property.objects.filter(user=request.user).aggregate(Sum("rates")).get("rates__sum")
    total_insurance = (
        Property.objects.filter(user=request.user).aggregate(Sum("insurance")).get("insurance__sum")
    )
    total_maintenance = (
        Property.objects.filter(user=request.user).aggregate(Sum("maintenance")).get("maintenance__sum")
    )
    total_management_fee = (
        Property.objects.filter(user=request.user)
        .aggregate(Sum("management_fee"))
        .get("management_fee__sum")
    )

    # total_operating_costs = total_rates + total_insurance + total_maintenance + total_management_fee
    total_cap_rate = ((total_noi * 52) / total_market_value) * 100
    total_loan_to_value = total_loan_amount / total_market_value * 100
    # total_rent = f"{total_rent:,}"

    context = {
        "object_list": qs,
        "total_market_value": total_market_value,
        "total_loan_amount": total_loan_amount,
        "total_loan_to_value": total_loan_to_value,
        "total_repayments": total_repayments / 52,
        "total_rent": total_rent,
        "total_operating_costs": total_operating_costs,
        "total_cap_rate": total_cap_rate,
        "total_noi": total_noi,
        "selected": selected,
    }
    return render(request, "properties/main.html", context)


def property_list_monthly(request):
    selected = "Monthly"
    qs = Property.objects.filter(user=request.user)
    total_operating_costs = 0
    total_noi = 0
    total_rent = 0
    for obj in qs:
        obj.rent_after_vacany_rate = obj.rent - (obj.rent * (obj.vacancy_rate / 100))
        obj.net_management = obj.rent_after_vacany_rate * (obj.management_fee / 100)
        obj.operating_cost = (
                obj.net_management
                + obj.insurance
                + obj.maintenance
                + obj.rates
                + obj.bodycorp_fee
        )
        obj.operating_cost = obj.operating_cost / 12
        obj.net_operating_income = obj.rent_after_vacany_rate - obj.operating_cost * 12
        obj.cap_rate = obj.net_operating_income / obj.market_value * 100
        obj.net_operating_income = obj.net_operating_income / 12
        obj.loan_to_value = int(obj.loan_amount) / int(obj.market_value) * 100
        obj.rent = obj.rent_after_vacany_rate / 12
        obj.repayments = round(obj.repayments / 12, 2)
        total_noi = total_noi + obj.net_operating_income
        total_operating_costs += obj.operating_cost
        total_rent = total_rent + obj.rent

    total_market_value = qs.aggregate(Sum("market_value")).get("market_value__sum")
    total_loan_amount = qs.aggregate(Sum("loan_amount")).get("loan_amount__sum")
    total_repayments = (
        Property.objects.filter(user=request.user).aggregate(Sum("repayments")).get("repayments__sum")
    )

    total_rates = Property.objects.filter(user=request.user).aggregate(Sum("rates")).get("rates__sum")
    total_insurance = (
        Property.objects.filter(user=request.user).aggregate(Sum("insurance")).get("insurance__sum")
    )
    total_maintenance = (
        Property.objects.filter(user=request.user).aggregate(Sum("maintenance")).get("maintenance__sum")
    )
    total_management_fee = (
        Property.objects.filter(user=request.user)
        .aggregate(Sum("management_fee"))
        .get("management_fee__sum")
    )

    # total_operating_costs = total_rates + total_insurance + total_maintenance + total_management_fee
    total_cap_rate = ((total_noi * 12) / total_market_value) * 100
    total_loan_to_value = total_loan_amount / total_market_value * 100
    # total_rent = f"{total_rent:,}"

    context = {
        "object_list": qs,
        "total_market_value": total_market_value,
        "total_loan_amount": total_loan_amount,
        "total_loan_to_value": total_loan_to_value,
        "total_repayments": total_repayments / 12,
        "total_rent": total_rent,
        "total_operating_costs": total_operating_costs,
        "total_cap_rate": total_cap_rate,
        "total_noi": total_noi,
        "selected": selected,
    }
    return render(request, "properties/main.html", context)


@login_required(login_url='/login/')
def property_detail_view(request, **kwargs):
    pk = kwargs.get("pk")

    obj = Property.objects.filter(user=request.user).get(pk=pk)
    contact_obj = Contact.objects.filter(properties=pk, user=request.user)

    reminders = Reminder.objects.filter(property=obj, user=request.user).order_by("due_date")
    reminders_count = reminders.count()

    nper_interest = float(obj.interest_rate / 100)
    nper_repayment = float(obj.repayments / 12)
    nper_loan_ammount = float(obj.loan_amount)
    loan_term_left = (
            np.round(
                npf.nper(nper_interest / 12, nper_repayment * -1, nper_loan_ammount), 5
            )
            / 12
    )

    equity = obj.market_value - obj.loan_amount

    rent_monthly = obj.rent / 12
    rent_weekly = obj.rent / 52

    rent_after_vacany_rate = obj.rent - (obj.rent * (obj.vacancy_rate / 100))
    rent_after_vancany_rate_weekly = rent_after_vacany_rate / 52
    rent_after_vacany_rate_monthly = rent_after_vacany_rate / 12
    net_management = rent_after_vacany_rate * (obj.management_fee / 100)

    operating_expenses = (
            obj.insurance + net_management + obj.maintenance + obj.rates + obj.bodycorp_fee
    )
    operating_expenses_monthly = operating_expenses / 12
    operating_expenses_weekly = operating_expenses / 52
    operating_expenses_percent = (operating_expenses / rent_after_vacany_rate) * 100

    net_operating_income = rent_after_vacany_rate - operating_expenses
    net_operating_income_monthly = net_operating_income / 12
    net_operating_income_weekly = net_operating_income / 52
    net_operating_income_percent = (net_operating_income / rent_after_vacany_rate) * 100

    cap_rate = (net_operating_income / obj.market_value) * 100
    gross_yield = (obj.rent / obj.market_value) * 100
    mortgage_repayment = obj.repayments
    mortgage_repayment_monthly = obj.repayments / 12
    mortgage_repayment_weekly = obj.repayments / 52

    net_income = net_operating_income - mortgage_repayment
    net_income_monthly = net_income / 12
    net_income_weekly = net_income / 52

    loan_to_value = obj.loan_amount / obj.market_value * 100
    context = {
        "object": obj,
        "contact_obj": contact_obj,
        "reminders": reminders,
        "reminders_count": reminders_count,
        "loan_term_left": loan_term_left,
        "equity": equity,
        "net_management": net_management,
        "rent_monthly": rent_monthly,
        "rent_weekly": rent_weekly,
        "rent_after_vacany_rate": rent_after_vacany_rate,
        "rent_after_vancany_rate_weekly": rent_after_vancany_rate_weekly,
        "rent_after_vacany_rate_monthly": rent_after_vacany_rate_monthly,
        "operating_expenses": operating_expenses,
        "operating_expenses_weekly": operating_expenses_weekly,
        "operating_expenses_monthly": operating_expenses_monthly,
        "operating_expenses_percent": operating_expenses_percent,
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


def sort(myList):
    myList.sort()
    return myList


@login_required(login_url='/login/')
def property_summary_view(request, year, *args, **kwargs):
    """
    Get Property objects for selected year
    """
    qs = Property.objects.filter(purchase_date__year=year, user=request.user)

    """
    Get retirement goals objects for selected year
    """

    retirement_goal = RetirementGoal.objects.filter(start_date__year=year, user=request.user)
    if retirement_goal:
        for retirement_goal in retirement_goal:
            goal_networth = float(retirement_goal.networth_goal)
            real_estate_percent = float(retirement_goal.real_estate / 100)
            commodities_percent = float(retirement_goal.commodities / 100)
            crypto_percent = float(retirement_goal.crypto / 100)
            stocks_percent = Decimal(retirement_goal.stocks / 100)
    else:
        goal_networth = None
        real_estate_percent = None
        commodities_percent = None
        crypto_percent = None
        stocks_percent = None
    print("stocks_percent", stocks_percent)

    """
    Show assets and liabilities in graph
    """
    graph_asset = 0
    graph_lib = 0

    """
    Set retirement goals and current value by tracking it yearly
    """
    if retirement_goal:
        start_year = retirement_goal.start_date.year
    else:
        start_year = None
    total_operating_expenses = 0

    # PV is present retirement networth goal, r is consumer price index(cpi) ratio
    PV = goal_networth
    if retirement_goal:
        r = float(retirement_goal.cpi)
    else:
        r = None
    n = 10

    def CurrentYearGoal():
        if start_year is not None:
            return date.today().year - start_year
        return None

    def FutureValue(x):
        if r is not None:
            return PV * (1 + r / 100) ** x
        return None

    """
    Estimate future value of current year goal networth
    """
    current_goal = FutureValue(CurrentYearGoal())
    if current_goal is not None:
        property_goal = real_estate_percent * current_goal
    else:
        property_goal = None
    total_rent_after_vacany_rate = 0

    """
    get each property objects data, calculate net value
    """
    for obj in qs:
        obj.rent_after_vacany_rate = obj.rent - (obj.rent * (obj.vacancy_rate / 100))
        obj.net_management = obj.rent_after_vacany_rate * (obj.management_fee / 100)
        obj.operating_cost = (
                obj.net_management
                + obj.insurance
                + obj.maintenance
                + obj.rates
                + obj.bodycorp_fee
        )
        total_operating_expenses += obj.operating_cost
        total_rent_after_vacany_rate += obj.rent_after_vacany_rate

    total_properties = qs.count()
    total_assets = qs.aggregate(Sum("market_value")).get("market_value__sum")
    total_liabilities = qs.aggregate(Sum("loan_amount")).get("loan_amount__sum")
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
    total_rent = total_rent_after_vacany_rate
    total_income = total_rent + total_other_income
    # total_networth = total_assets - total_liabilities
    total_networth = 10000

    # total_expenses = total_operating_expenses + total_repayments
    total_expenses = 2000

    total_net_rental_income = total_income - total_expenses
    if property_goal is not None:
        property_progress = total_networth / property_goal * 100
    else:
        property_progress = None
    if total_repayments is not None:
        loan_to_debt_ratio = total_income / total_repayments
        loan_to_debt_percent = (total_repayments / total_income) * 100

        debt_service_coverage_ratio = (
                                              total_income - total_operating_expenses
                                      ) / total_repayments
        debt_service_coverage_percent = (
                                                total_repayments / (total_income - total_operating_expenses)
                                        ) * 100
    else:
        loan_to_debt_ratio = None
        loan_to_debt_percent = None
        debt_service_coverage_ratio = None
        debt_service_coverage_percent = None
    if total_income != 0 and total_expenses != 0:
        break_even_point = (total_expenses / total_income) * 100
    else:
        break_even_point = 0

    """
        Stocks Calculations::
        ** get equites total 
        ** get bonds total
        ** get cce total
        ** get commodities total
        ** get reits total
    """
    stocks_qs = IndexFund.objects.filter(date__year=year, user=request.user)
    stocks_total_value = 0
    stocks_total_equities = 0
    stocks_total_bonds = 0
    stocks_total_cce = 0
    stocks_total_commodites = 0
    stocks_total_diversified = 0
    stocks_total_reits = 0
    stocks_total_other = 0

    for obj in stocks_qs:
        obj.value = round(obj.shares * obj.share_price, 2)
        stocks_total_value = stocks_total_value + obj.value
        if obj.asset_class == "Equities":
            stocks_total_equities = stocks_total_equities + obj.value
        if obj.asset_class == "Bonds":
            stocks_total_bonds = stocks_total_bonds + obj.value
        if obj.asset_class == "Cash & Cash Equivalents":
            stocks_total_cce = stocks_total_cce + obj.value
        if obj.asset_class == "Commodites":
            stocks_total_commodites = stocks_total_commodites + obj.value
        if obj.asset_class == "Diversified":
            stocks_total_diversified = stocks_total_diversified + obj.value
        if obj.asset_class == "Reits":
            stocks_total_reits = stocks_total_reits + obj.value
        if obj.asset_class == "Other":
            stocks_total_other = stocks_total_other + obj.value
    # Adding retirement's networth current goal and stocks percent
    print("stocks_total_value", stocks_total_value)
    if stocks_percent is not None:
        stocks_goal = Decimal(stocks_percent) * Decimal(current_goal)
        stocks_total_progress = 0
        stocks_total_progress1 = float(stocks_total_value / stocks_goal) * 100
        print("stocks_total_progress1", stocks_total_progress1)
        if stocks_goal > 0 and stocks_total_progress1 > 0:
            stocks_total_progress += stocks_total_progress1
        else:
            stocks_total_progress = 0

    # Commodities
    commodities = Commodity.objects.filter(user=request.user)
    # commodities_total_amount = 0
    # invested_total = 0
    # for commodity in commodities:
    #     commodity.totalweight = 0
    #     commodity.invested = 0
    #     transactions = Transaction.objects.filter(
    #         commodity=commodity.pk, date__year=year
    #     )
    #     for transaction in transactions:
    #         if transaction.transaction_type == "Buy":
    #             commodity.totalweight += transaction.weight
    #             commodity.invested += transaction.value
    #         if transaction.transaction_type == "Sell":
    #             commodity.totalweight -= transaction.weight
    #             commodity.invested -= transaction.value
    #     commodity.total = commodity.totalweight * commodity.spot_price
    #     commodities_total_amount += commodity.total
    #     invested_total += commodity.invested
    grand_total = 0
    print(current_goal)
    if current_goal is not None:
        commodities_goal = float(commodities_percent * current_goal)
        # commodities_progress1 = float(commodities_total_amount) / commodities_goal * 100
        commodities_progress1 = float(20000) / commodities_goal * 100
        commod_progress = 0.0
        if commodities_goal > 0 and commodities_progress1 > 0:
            commod_progress += commodities_progress1
        else:
            commod_progress = 0.0

        # Crypto
        try:
            crypto_qs = Crypto.objects.filter(user=request.user)
        except Crypto.objects.filter(user=request.user).DoesNotExist:
            crypto_qs = None
        crypto_total_amount = 0
        # for item in crypto_qs:
        #     item.total = item.quantity * item.spot_price
        #     crypto_total_amount += item.total
        crypto_goal = float(crypto_percent * current_goal)

        if crypto_goal > 0:
            crypto_progress = float(crypto_total_amount) / crypto_goal * 100
        else:
            crypto_progress = 0
    else:
        crypto_total_amount = 0
    # Personal Balance Sheet
    pba_qs = PersonalBalance.objects.filter(entry_type="Asset", date__year=year, user=request.user)
    pbl_qs = PersonalBalance.objects.filter(entry_type="Liability", date__year=year, user=request.user)
    total_pb_assets = pba_qs.aggregate(Sum("amount")).get("amount__sum")
    total_pb_liabilities = pbl_qs.aggregate(Sum("amount")).get("amount__sum")
    if total_pb_assets is None:
        total_pb_assets = 0
    if total_pb_liabilities is None:
        total_pb_liabilities = 0
    qs_save = PersonalBalance.objects.filter(entry_type="Savings", date__year=year, user=request.user)
    savings_total = 0
    for item in qs_save:
        savings_total = savings_total + item.amount

    qs_retirement = PersonalBalance.objects.filter(
        entry_type="Retirement Acc", date__year=year, user=request.user
    )
    total_retirement = 0
    for item in qs_retirement:
        total_retirement = total_retirement + item.amount

    pb_networth = (
            total_pb_assets + savings_total + total_retirement - total_pb_liabilities
    )
    cf_income_yearly = 0
    cf_expense_yearly = 0
    cf_income_qs = CashFlow.objects.filter(entry_type="Income", date__year=year, user=request.user)
    cf_expense_qs = CashFlow.objects.filter(entry_type="Expense", date__year=year, user=request.user)

    for item in cf_income_qs:
        if item.frequency == "Weekly":
            item.amount = item.amount * 52
            item.amount = round(item.amount, 2)
        if item.frequency == "Monthly":
            item.amount = item.amount * 12
            item.amount = round(item.amount, 2)
        elif item.frequency == "Fortnightly":
            item.amount = item.amount * 26
            item.amount = round(item.amount, 2)
        cf_income_yearly = cf_income_yearly + item.amount

    for item in cf_expense_qs:
        if item.frequency == "Weekly":
            item.amount = item.amount * 52
            item.amount = round(item.amount, 2)
        if item.frequency == "Monthly":
            item.amount = item.amount * 12
            item.amount = round(item.amount, 2)
        elif item.frequency == "Fortnightly":
            item.amount = item.amount * 26
            item.amount = round(item.amount, 2)
        cf_expense_yearly = cf_expense_yearly + item.amount

    cf_cashflow = cf_income_yearly - cf_expense_yearly

    """
    ###### Display assets, liabilities and networth of all years on chart ######
    """
    """
    extracted all Years from Database 
    """
    years = list(Property.objects.filter(user=request.user).values_list("purchase_date__year").distinct())
    print(years, 'yearssd')
    years_list = []
    for data in years:
        for item in data:
            years_list.append(item)
    years_list = sort(years_list)

    yearwise_graph_assets = []
    yearwise_graph_libs = []
    yearwise_networths = []

    """
    Get all years records from apps
    """
    for my_year in years_list:
        props_qs = Property.objects.filter(purchase_date__year=my_year, user=request.user)
        yearwise_props_assets = props_qs.aggregate(Sum("market_value")).get("market_value__sum")
        print(yearwise_props_assets, "asdfasdf")
        yearwise_props_liabilities = props_qs.aggregate(Sum("loan_amount")).get(
            "loan_amount__sum"
        )

        pba_qs = PersonalBalance.objects.filter(entry_type="Asset", date__year=my_year, user=request.user)
        pbl_qs = PersonalBalance.objects.filter(
            entry_type="Liability", date__year=my_year
        )
        qs_save = PersonalBalance.objects.filter(entry_type="Savings", date__year=year, user=request.user)
        qs_retirement = PersonalBalance.objects.filter(
            entry_type="Retirement Acc", date__year=year, user=request.user
        )

        yearwise_pb_assets = pba_qs.aggregate(Sum("amount")).get("amount__sum")
        yearwise_pb_liabilities = pbl_qs.aggregate(Sum("amount")).get("amount__sum")
        yearwise_pb_save = qs_save.aggregate(Sum("amount")).get("amount__sum")
        yearwise_pb_qs_retirement = qs_retirement.aggregate(Sum("amount")).get(
            "amount__sum"
        )
        print("qadeer")
        yearwise_crypto_qs = Crypto.objects.filter(user=request.user)
        crypto_total_value = 0
        # for item in yearwise_crypto_qs:
        #     item.total = item.quantity * item.spot_price
        #     crypto_total_value += item.total

        yearwise_stocks_qs = IndexFund.objects.filter(date__year=my_year, user=request.user)
        stocks_total_value = 0
        for obj in yearwise_stocks_qs:
            obj.value = round(obj.shares * obj.share_price, 2)
            stocks_total_value = stocks_total_value + obj.value

        # commod_qs = Commodity.objects.all()
        # commodities_total_value = 0
        # for item in commod_qs:
        #     item.totalweight = 0
        #     yearwise_commod_qs2 = Transaction.objects.filter(
        #         commodity=item.pk, date__year=my_year
        #     )
        #     for items in yearwise_commod_qs2:
        #         if items.transaction_type == "Buy":
        #             item.totalweight += items.weight
        #         if items.transaction_type == "Sell":
        #             item.totalweight -= items.weight
        #     item.total = item.totalweight * item.spot_price
        #     commodities_total_value += item.total
        if yearwise_props_assets is not None and yearwise_pb_assets is not None:
            if yearwise_pb_save is not None and yearwise_pb_qs_retirement is not None:
                if crypto_total_value is not None and stocks_total_value is not None:
                    yearwise_graph_asset = (
                            yearwise_props_assets
                            + yearwise_pb_assets
                            + yearwise_pb_save
                            + yearwise_pb_qs_retirement
                            + crypto_total_value
                            + stocks_total_value
                            + 10000
                    )
                    yearwise_graph_lib = yearwise_props_liabilities + yearwise_pb_liabilities
                    yearwise_networth = yearwise_graph_asset - yearwise_graph_lib

                    yearwise_graph_assets.append(float(yearwise_graph_asset))
                    yearwise_graph_libs.append(float(yearwise_graph_lib))
                    yearwise_networths.append(float(yearwise_networth))
        """
        Single selected Year graph assets, liabilities and networth.
        """
    print(total_pb_assets, total_pb_assets, savings_total, total_retirement, stocks_total_value, crypto_total_amount)
    if total_assets is not None:
        graph_asset = (
                total_assets
                + total_pb_assets
                + savings_total
                + total_retirement
                + stocks_total_value
                + 2000
                + crypto_total_amount
        )
    else:
        graph_asset = (
                total_pb_assets
                + savings_total
                + total_retirement
                + stocks_total_value
                + 2000
                + crypto_total_amount
        )
    print(total_liabilities, total_pb_assets)
    if total_liabilities is not None and total_pb_liabilities is not None:
        graph_lib = total_liabilities + total_pb_liabilities
    else:
        graph_lib = 0
    graph_nw = graph_asset - graph_lib
    context = {
        "object_list": qs,
        "year": year,
        "total_properties": total_properties,
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "total_networth": total_networth,
        "total_rent": total_rent,
        "total_income": total_income,
        "total_other_income": total_other_income,
        "total_operating_expenses": total_operating_expenses,
        "total_repayments": total_repayments,
        "total_expenses": total_expenses,
        "total_net_rental_income": total_net_rental_income,
        "loan_to_debt_ratio": loan_to_debt_ratio,
        "loan_to_debt_percent": loan_to_debt_percent,
        "debt_service_coverage_ratio": debt_service_coverage_ratio,
        "debt_service_coverage_percent": debt_service_coverage_percent,
        "break_even_point": break_even_point,
        "total_pb_assets": total_pb_assets,
        "total_pb_liabilities": total_pb_liabilities,
        "savings_total": savings_total,
        "total_retirement": total_retirement,
        "pb_networth": pb_networth,
        "cf_income_yearly": cf_income_yearly,
        "cf_expense_yearly": cf_expense_yearly,
        "cf_cashflow": cf_cashflow,
        "stocks_total_value": stocks_total_value,
        "stocks_total_equities": stocks_total_equities,
        "stocks_total_bonds": stocks_total_bonds,
        "stocks_total_cce": stocks_total_cce,
        "stocks_total_commodites": stocks_total_commodites,
        "stocks_total_diversified": stocks_total_diversified,
        "stocks_total_reits": stocks_total_reits,
        "stocks_total_other": stocks_total_other,
        "commodities": commodities,
        "commodities_total_value": 200,
        "crypto_total_amount": crypto_total_amount,
        "property_progress": property_progress,
        # Single year context for assets, liabilities and networth
        "graph_asset": graph_asset,
        "graph_lib": graph_lib,
        "graph_nw": graph_nw,
        # ALL Years list of assets, liabilities and networth
        "years_list": years_list,
        "yearwise_graph_assets": yearwise_graph_assets,
        "yearwise_graph_libs": yearwise_graph_libs,
        "yearwise_networths": yearwise_networths,
    }
    return render(request, "properties/summary.html", context)


def addproperty(request):
    if request.method == "POST":
        print("Adding", request.body)
        propertyData = json.loads(request.body)
        form= PropertyForm(
            name=propertyData['name'],
            property_type=propertyData["type"],
            land_size=int(propertyData['land_size']),
            building_size=propertyData['building_size'],
            lounge=propertyData['lounge'],
            bedrooms=propertyData['bedrooms'],
            bathrooms=propertyData['bathrooms'],
            parking=propertyData['parking'],
            garage=propertyData["Garage"],
            vacancy_rate=propertyData["vacancy_rate"],
            street_address=propertyData["address"],
            purchase_date=propertyData["date"],
            market_value=propertyData["market_value"],
            purchase_price=propertyData["purchase_price"],
            deposit=propertyData["deposit"],
            loan_amount=propertyData["loan_amount"],
            loan_term=propertyData["loan_amount"],
            interest_rate=propertyData["interest_rate"],
            repayments=propertyData["repayments"],
            rates=propertyData["rates"],
            rent=propertyData["rent"],
            bodycorp_fee=propertyData["body_corp_fee"],
            management_fee=propertyData["management_fee"],
            insurance=propertyData["insurance"],
            maintenance=propertyData["maintenance"],
            user=request.user
        )
        if form.is_valid():
            form.save()
        else:
            print(form.errors,"error")
        # obj = Property.objects.create(
        #     name=propertyData['name'],
        #     property_type=propertyData["type"],
        #     land_size=int(propertyData['land_size']),
        #     building_size=propertyData['building_size'],
        #     lounge=propertyData['lounge'],
        #     bedrooms=propertyData['bedrooms'],
        #     bathrooms=propertyData['bathrooms'],
        #     parking=propertyData['parking'],
        #     garage=propertyData["Garage"],
        #     vacancy_rate=propertyData["vacancy_rate"],
        #     street_address=propertyData["address"],
        #     purchase_date=propertyData["date"],
        #     market_value=propertyData["market_value"],
        #     purchase_price=propertyData["purchase_price"],
        #     deposit=propertyData["deposit"],
        #     loan_amount=propertyData["loan_amount"],
        #     loan_term=propertyData["loan_amount"],
        #     interest_rate=propertyData["interest_rate"],
        #     repayments=propertyData["repayments"],
        #     rates=propertyData["rates"],
        #     rent=propertyData["rent"],
        #     bodycorp_fee=propertyData["body_corp_fee"],
        #     management_fee=propertyData["management_fee"],
        #     insurance=propertyData["insurance"],
        #     maintenance=propertyData["maintenance"],
        #     user=request.user
        # )

        # user = {'id': obj.id, 'ticker': obj.ticker, 'quantity': obj.quantity, 'name': obj.name}

        data = {
            'user': "data is saved"
        }
        return JsonResponse(data)


def add_property(request):
    submitted = False
    if request.method == "POST":
        form = PropertyForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    else:
        form = PropertyForm
        if "submitted" in request.GET:
            submitted = True
    form = PropertyForm
    return render(
        request, "properties/add.html", {"form": form, "submitted": submitted}
    )


def editproperty(request):
    if request.method == "POST":
        propertyData = json.loads(request.body)
        property = Property.objects.filter(user=request.user).get(id=propertyData['id'])
        print(propertyData, 'propertyData')
        print(property, 'property')
        print(propertyData['land_size'], 'land_size')
        property.name = propertyData['name']
        property.property_type = propertyData['type']
        property.land_size = int(propertyData['land_size'])
        property.building_size = propertyData['building_size']
        property.lounge = propertyData['lounge']
        property.bedrooms = propertyData['bedrooms']
        property.bathrooms = propertyData['bathrooms']
        property.parking = propertyData['parking']
        property.garage = propertyData['Garage']
        property.vacancy_rate = propertyData['vacancy_rate']
        property.purchase_price = propertyData['purchase_price']
        property.market_value = propertyData['market_value']
        property.deposit = propertyData['deposit']
        property.loan_amount = propertyData['loan_amount']
        property.loan_term = propertyData['loan_term']
        property.interest_rate = propertyData['interest_rate']
        property.repayments = propertyData['repayments']
        property.rates = propertyData['rates']
        property.rent = propertyData['rent']
        property.bodycorp_fee = propertyData['body_corp_fee']
        property.management_fee = propertyData['management_fee']
        property.insurance = propertyData['insurance']
        property.maintenance = propertyData['maintenance']
        property.save()
        data = {
            'user': "data is updated"
        }
        return JsonResponse(data)


def update_property(request, pk):
    property = Property.objects.filter(user=request.user).get(id=pk)
    form = PropertyForm(instance=property)

    if request.method == "POST":
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close()</script>'
            )
    context = {"form": form}
    return render(request, "properties/add.html", context)


def deleteproperty(request):
    id1 = request.GET.get('id', None)
    print(id1, "delete")
    Property.objects.filter(user=request.user).get(id=id1).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)


def delete_property(request, pk):
    property = Property.objects.filter(user=request.user).get(id=pk)
    qs = Property.objects.filter(user=request.user).get(id=pk)
    context = {
        "object": qs,
    }

    if request.method == "POST":
        # delete object
        property.delete()
        # after deleting redirect to
        # home page
        return HttpResponse('<script type="text/javascript">window.close()</script>')
    return render(request, "properties/delete_property.html", context)
