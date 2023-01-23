import json
import datetime
from decimal import Decimal
from yahooquery import Ticker
from django.shortcuts import render, redirect, get_object_or_404
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
from django.views.decorators.http import require_POST

from incomestatements.models import Category
from incomestatements_property.models import PropertyCategory
from stock_portfolios.models import Stock
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
    etf_summary = index_funds_summary(request, year)
    all_summary = overall_summary(request, year)
    prop_summary = property_summary(request, year)
    pers_summary = personal_summary(request, year)
    cash_summary = cashflow_summary(request, year)
    comm_summary = commodity_summary(request, year)
    cryp_summary = crypto_summary(request, year)
    crypto = cryp_summary["crypto_total_amount"]
    stock = etf_summary["stock_total_amount"]
    etf = etf_summary["etf_total_amount"]
    commodity = comm_summary["commodities_total_value"]
    asset = prop_summary["assets"]
    total = crypto + stock + asset + commodity + etf
    asset_pie = 0
    crypto_pie = 0
    stock_pie = 0
    etf_pie = 0
    commodity_pie = 0
    print(total,'total')
    if total != 0:
        asset_pie = (asset / total) * 100
        crypto_pie = (crypto / total) * 100
        stock_pie = (stock / total) * 100
        etf_pie = (etf / total) * 100
        commodity_pie = (commodity / total) * 100
    context = {
        # overall summary
        "all_assets": all_summary["all_assets"],
        "all_liabilities": all_summary["all_liabilities"],
        "all_networth": all_summary["all_networth"],
        "years_list": all_summary["year_list"],
        "asset_pie": round(asset_pie, 2),
        "crypto_pie": round(crypto_pie, 2),
        "stock_pie": round(stock_pie, 2),
        "commodity_pie": round(commodity_pie, 2),
        "etf_pie": round(etf_pie, 2),
        # property summary
        "property_progress": prop_summary['progress_bar'],
        "total_properties": prop_summary['no_of_properties'],
        "total_assets": prop_summary["assets"],
        "total_liabilities": prop_summary["liabilities"],
        "total_networth": prop_summary["networth"],
        "total_income": prop_summary["income"],
        "total_rent": prop_summary["rent_income"],
        "total_other_income": prop_summary["other_income"],
        "total_expenses": prop_summary["expense"],
        "total_operating_expenses": prop_summary["operating_expenses"],
        "total_repayments": prop_summary["repayments"],
        "total_net_rental_income": prop_summary["income"] - prop_summary["expense"],
        "loan_to_debt_ratio": prop_summary["loan_to_debt_ratio"],
        "debt_service_coverage_ratio": prop_summary["debt_service_coverage_ratio"],
        "break_even_point": prop_summary['break_even_point'],
        # personal_summary
        "total_pb_assets": pers_summary['assets'],
        "savings_total": pers_summary['savings'],
        "total_retirement": pers_summary['retirement'],
        "total_pb_liabilities": pers_summary['liabilities'],
        "pb_networth": pers_summary["networth"],
        # cashflow summary
        "cf_income_yearly": cash_summary['income'],
        "cf_expense_yearly": cash_summary['expense'],
        "cf_cashflow": cash_summary['total'],
        # the market
        # commodities
        "commodities": comm_summary['commodities'],
        "commodities_total_value": comm_summary["commodities_total_value"],
        "commodities_prog": comm_summary['commodities_prog'],
        # crypto
        "crypto_qs": cryp_summary["crypto_qs"],
        "crypto_total_amount": cryp_summary["crypto_total_amount"],
        "crypto_progress": cryp_summary["crypto_progress"],
        # Index Funds / ETF
        "etf_qs": etf_summary["etf_qs"],
        "stocks_total_value": etf_summary["etf_total_amount"],
        "stocks_total_progress": etf_summary["etf_progress"],
        "stocks_total_equities": etf_summary["stocks_total_equities"],
        "stocks_total_bonds": etf_summary["stocks_total_bonds"],
        "stocks_total_cce": etf_summary["stocks_total_cce"],
        "stocks_total_diversified": etf_summary["stocks_total_diversified"],
        "stocks_total_reits": etf_summary["stocks_total_reits"],
        "stocks_total_other": etf_summary["stocks_total_other"],
        "stock_total_amount": etf_summary["stock_total_amount"],
    }
    return render(request, "properties/summary.html", context)


def overall_summary(request, year):
    etf_summary = index_funds_summary(request, year)
    comm_summary = commodity_summary(request, year)
    cryp_summary = crypto_summary(request, year)
    property = sum(data.market_value for data in Property.objects.filter(user=request.user))
    liability = sum(data.loan_amount for data in Property.objects.filter(user=request.user))

    all_assets = round(property + cryp_summary['crypto_total_amount'] + etf_summary['stock_total_amount'] + etf_summary[
        'etf_total_amount'] + comm_summary['commodities_total_value'], 2)
    all_liabilities = [round(liability, 2)]
    networth = all_assets - liability
    assets = [all_assets]
    all_networth = [networth]
    year_list = [int(year)]
    context = {
        "all_assets": assets,
        "all_liabilities": all_liabilities,
        "all_networth": all_networth,
        "year_list": year_list,
    }
    return context


def get_stock_price_data(tickers):
    all_symbols = " ".join(tickers)
    myInfo = Ticker(all_symbols)
    data = myInfo.price
    result = dict.fromkeys(data.keys())
    for key, value in data.items():
        result[key] = value['regularMarketPrice']
    return result


def index_funds_summary(request, year):
    stock_data = Stock.objects.filter(user=request.user, year=year, stock_ticker__stock_type='INDIVIDUAL')
    etf_data = Stock.objects.filter(user=request.user, year=year, stock_ticker__stock_type='INDEX_FUND/EFT')
    financial_plan_data = RetirementGoal.objects.filter(user=request.user, start_date__year=year).values()
    used_stocks_ticker = stock_data.values_list('stock_ticker__ticker', flat=True).distinct()
    stock_prices = get_stock_price_data(used_stocks_ticker)
    used_stocks_ticker_etf = etf_data.values_list('stock_ticker__ticker', flat=True).distinct()
    stock_prices_etf = get_stock_price_data(used_stocks_ticker_etf)
    print(etf_data, 'etf_data')
    etf_total_amount = 0
    etf_progress = 0
    stocks_total_equities = 0
    stocks_total_bonds = 0
    stocks_total_cce = 0
    stocks_total_diversified = 0
    stocks_total_reits = 0
    stocks_total_other = 0
    stock_total_amount = 0
    if stock_data:
        stock_total_amount = sum(data.quantity * stock_prices[data.stock_ticker.ticker] for data in stock_data)
    if etf_data:
        etf_total_amount = sum(data.quantity * stock_prices_etf[data.stock_ticker.ticker] for data in etf_data)
        stocks_total_equities = sum(
            data.quantity * stock_prices_etf[data.stock_ticker.ticker] for data in
            etf_data.filter(stock_ticker__stock_category="EQUITIES"))
        stocks_total_bonds = sum(
            data.quantity * stock_prices_etf[data.stock_ticker.ticker] for data in
            etf_data.filter(stock_ticker__stock_category="BONDS"))
        stocks_total_cce = sum(
            data.quantity * stock_prices_etf[data.stock_ticker.ticker] for data in
            etf_data.filter(stock_ticker__stock_category="CASH_AND_CASH_EQUIVALENT"))
        stocks_total_diversified = sum(
            data.quantity * stock_prices_etf[data.stock_ticker.ticker] for data in
            etf_data.filter(stock_ticker__stock_category="DIVERSIFIED"))
        stocks_total_reits = sum(
            data.quantity * stock_prices_etf[data.stock_ticker.ticker] for data in
            etf_data.filter(stock_ticker__stock_category="REITS"))
        stocks_total_other = sum(data.quantity * stock_prices_etf[data.stock_ticker.ticker] for data in
                                 etf_data.filter(stock_ticker__stock_category="OTHERS"))
    if financial_plan_data:
        if financial_plan_data[0]["stocks"] != 0 and financial_plan_data[0]["stocks"] is not None:
            financial_data = float(financial_plan_data[0]["stocks"] / 100) * float(
                financial_plan_data[0]["networth_goal"])
            etf_progress = (etf_total_amount / financial_data) * 100
    context = {
        "etf_qs": etf_data,
        "etf_total_amount": etf_total_amount,
        "etf_progress": etf_progress,
        "stocks_total_equities": stocks_total_equities,
        "stocks_total_bonds": stocks_total_bonds,
        "stocks_total_cce": stocks_total_cce,
        "stocks_total_diversified": stocks_total_diversified,
        "stocks_total_reits": stocks_total_reits,
        "stocks_total_other": stocks_total_other,
        "stock_total_amount": stock_total_amount
    }
    return context


def get_crypto_price_data(tickers):
    all_symbols = " ".join(tickers)
    myInfo = Ticker(all_symbols)
    data = myInfo.price
    result = dict.fromkeys(data.keys())
    print(data, 'data')
    for key, value in data.items():
        result[key] = value['regularMarketPrice']
        print(result, 'result')
    return result


def crypto_summary(request, year):
    crypto_data = Crypto.objects.filter(user=request.user, year=year)
    financial_plan_data = RetirementGoal.objects.filter(user=request.user, start_date__year=year).values()
    used_cryptos_ticker = crypto_data.values_list('crypto_ticker__ticker', flat=True).distinct()
    crypto_prices = get_crypto_price_data(used_cryptos_ticker)
    crypto_total_amount = 0
    crypto_progress = 0
    if crypto_data:
        crypto_total_amount = sum(data.quantity * crypto_prices[data.crypto_ticker.ticker] for data in crypto_data)
        for crypto in crypto_data:
            crypto.investment = crypto.quantity * crypto_prices[crypto.crypto_ticker.ticker]
    if financial_plan_data:
        if financial_plan_data[0]["crypto"] != 0 and financial_plan_data[0]["crypto"] is not None:
            financial_data = float(financial_plan_data[0]["crypto"] / 100) * float(
                financial_plan_data[0]["networth_goal"])
            crypto_progress = (crypto_total_amount / financial_data) * 100

    print(crypto_data, 'crypto_data')
    context = {"crypto_qs": crypto_data, "crypto_total_amount": crypto_total_amount, "crypto_progress": crypto_progress}
    return context


def get_commodities():
    commodities_list = [
        'GC=F',
        'SI=F',
        'PL=F',
        "PA=F"
    ]
    all_symbols = " ".join(commodities_list)
    myInfo = Ticker(all_symbols)
    data = myInfo.price
    result = dict.fromkeys(data.keys())
    for key, value in data.items():
        result[key] = value['regularMarketPrice']
    return result


def commodity_summary(request, year):
    commodity_data = Commodity.objects.filter(user=request.user, year=year)
    financial_plan_data = RetirementGoal.objects.filter(user=request.user, start_date__year=year).values()
    commodities_total_value = sum(data.investment for data in commodity_data)
    commodities = {
        1: "Gold", 2: "Silver", 3: "Platinum", 4: "Palladium",
    }
    commodity_prices = get_commodities()
    commodities_total_value = 0
    if commodity_data:
        commodities_total_value = sum(
            data.weight * commodity_prices[data.commodity_class.commodity_class] for data in commodity_data)
    arr = []
    for i in range(1, 5):
        com = {
            "commodity_class": commodities[i],
            "total": sum(data.weight * commodity_prices[data.commodity_class.commodity_class] for data in
                         commodity_data.filter(commodity_class__name=commodities[i]))
        }
        arr.append(com)
    commodities_prog = 0
    if financial_plan_data:
        if financial_plan_data[0]["commodities"] != 0 and financial_plan_data[0]["commodities"] is not None:
            financial_data = float(financial_plan_data[0]["commodities"] / 100) * float(
                financial_plan_data[0]["networth_goal"])
            commodities_prog = (commodities_total_value / financial_data) * 100
    context = {
        "commodities_total_value": commodities_total_value,
        "commodities": arr,
        "commodities_prog": commodities_prog
    }
    return context


def cashflow_summary(request, year):
    cashflow_data = Category.objects.filter(user=request.user, year=year)
    income = sum(data.compute_budget() for data in cashflow_data.filter(transaction_type="Income"))
    expense = sum(data.compute_budget() for data in cashflow_data.filter(transaction_type="Expense"))
    print(cashflow_data, 'cash')
    context = {
        "income": income,
        "expense": expense,
        "total": income - expense,
    }
    return context


def personal_summary(request, year):
    personal_data = PersonalBalance.objects.filter(user=request.user, date__year=year)
    print(personal_data)
    assets = sum(data.amount for data in personal_data.filter(entry_type="Asset"))
    savings = sum(data.amount for data in personal_data.filter(entry_type="Savings"))
    retirement = sum(data.amount for data in personal_data.filter(entry_type="Retirement Acc"))
    liabilities = sum(data.amount for data in personal_data.filter(entry_type="Liability"))
    context = {
        "assets": assets,
        "savings": savings,
        "retirement": retirement,
        "liabilities": liabilities,
        "networth": (assets + savings + retirement) - liabilities,
    }
    return context


def property_summary(request, year):
    property_data = Property.objects.filter(user=request.user)
    financial_plan_data = RetirementGoal.objects.filter(user=request.user, start_date__year=year).values()
    print(property_data)
    # property_summary
    progress_bar = 0
    assets = 0
    liabilities = 0
    networth = 0
    income = 0
    rent_income = 0
    other_income = 0
    expense = 0
    operating_expenses = 0
    repayments = 0
    loan_to_debt_ratio = 0
    debt_service_coverage_ratio = 0
    break_even_point = 0
    if property_data and financial_plan_data:
        property_networth = 0
        for data in property_data:
            property_networth += data.purchase_price
            assets += data.market_value
            liabilities += data.loan_amount
            rent_after_vacancy_rate = data.rent - (data.rent * (data.vacancy_rate / 100))
            income += rent_after_vacancy_rate + data.other_income
            rent_income += data.rent
            other_income += data.other_income
            operating_expenses += data.insurance + data.management_fee + data.maintenance + data.rates
            repayments += data.repayments
            expense += data.repayments + data.insurance + data.management_fee + data.maintenance + data.rates
        if financial_plan_data[0]['networth_goal'] is not None and financial_plan_data[0]['networth_goal'] != 0:
            progress_bar = (property_networth / financial_plan_data[0]['networth_goal']) * 100
        if income is not None and income != 0:
            loan_to_debt_ratio = (repayments / income)
            break_even_point = (expense / income) * 100
        if income is not None and operating_expenses is not None and income - operating_expenses != 0:
            debt_service_coverage_ratio = (repayments / (income - operating_expenses))
        networth = assets - liabilities
    # end of property_summary

    context = {
        "progress_bar": float(progress_bar),
        "no_of_properties": len(property_data),
        "assets": assets,
        "liabilities": liabilities,
        "networth": networth,
        "income": income,
        "rent_income": rent_income,
        "other_income": other_income,
        "expense": expense,
        "operating_expenses": operating_expenses,
        "repayments": repayments,
        "loan_to_debt_ratio": loan_to_debt_ratio,
        "debt_service_coverage_ratio": debt_service_coverage_ratio,
        "break_even_point": break_even_point,
    }
    return context


def addproperty(request):
    if request.method == "POST":
        print("Adding", request.body)
        propertyData = json.loads(request.body)
        form = PropertyForm(
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
            print(form.errors, "error")
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
    if request.method == "POST":
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.user = request.user
            property.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "propertyListChanged": None,
                        "showMessage": f"{property.name} added."
                    })
                })
    else:
        form = PropertyForm()
    return render(request, "properties/property_form.html", {"form": form})


def main(request):
    return render(request, 'properties/main.html')


def property_list(request):
    selected = "Yearly"
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
    return render(request, 'properties/property_list.html', context=context)


def edit_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == "POST":
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            property = form.save(commit=False)
            property.user = request.user
            property.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "propertyListChanged": None,
                        "showMessage": f"{property.name} updated."
                    })
                }
            )
    else:
        form = PropertyForm(instance=property)
    return render(request, 'properties/property_form.html', {
        'form': form,
        'property': property,
    })


def remove_property(request, pk):
    if request.method == 'GET':
        print('asf')
    property = get_object_or_404(Property, pk=pk)
    property.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "propertyListChanged": None,
                "showMessage": f"{property.name} deleted."
            })
        })
