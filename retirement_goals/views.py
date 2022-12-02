import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from retirement_goals.models import RetirementGoal
from .forms import RetirementGoalForm
import datetime
from datetime import date


def add_retirement_goal(request):
    if request.method == "POST":
        categoryData = json.loads(request.body)
        obj = RetirementGoal.objects.create(
            start_date=categoryData['start_date'],
            networth_goal=categoryData["networth_goal"],
            cpi=categoryData["cpi"],
            real_estate=categoryData["real_estate"],
            stocks=categoryData["stocks"],
            crypto=categoryData["crypto"],
            commodities=categoryData["commodities"],
            collectables=categoryData["collectables"],
            cash=categoryData["cash"],
            real_estate_swr=categoryData["real_estate_swr"],
            stocks_swr=categoryData["stocks_swr"],
            user=request.user
        )
        user = {
            'name': obj.networth_goal,
        }
        data = {
            'user': user
        }
        print(data, 'data')
        return JsonResponse(data)


# Create your views here.
def update_retirementgoal(request, year):
    retirementgoals = RetirementGoal.objects.filter(user=request.user)
    if retirementgoals:
        for retirementgoal in retirementgoals:
            print(retirementgoal, "retirementgoal")
            goal = retirementgoal.networth_goal
            start_year = retirementgoal.start_date.year
            current_year = date.today().year
            display_years = current_year - start_year + 1
            real_estate = retirementgoal.real_estate
            stocks = retirementgoal.stocks
            crypto = retirementgoal.crypto
            commodities = retirementgoal.commodities
            collectables = retirementgoal.collectables
            cash = retirementgoal.cash
            real_estate_swr = retirementgoal.real_estate_swr
            stocks_swr = retirementgoal.stocks_swr
            years = []
            goals = []
            realstate_FV = []
            stocks_FV = []
            crypto_FV = []
            commodities_FV = []
            collectables_FV = []
            cash_FV = []
            amount_FV = []
            PV = goal
            r = retirementgoal.cpi
            n = 10

            def CurrentYearGoal():
                return date.today().year - start_year

            def FutureValue(x):
                return PV * (1 + r / 100) ** x

            adjusted_goal = int(FutureValue(CurrentYearGoal()))
            print(adjusted_goal)
            print(CurrentYearGoal())
            current_goal = FutureValue(CurrentYearGoal())

            for x in range(11):
                years.append(str(start_year))
                start_year += 1
            for x in range(11):
                current_goal = int(PV * (1 + r / 100) ** x)
                goals.append(current_goal)
                real_estate_FV_value = int(current_goal * (real_estate / 100))
                stocks_FV_value = int(current_goal * (stocks / 100))
                realstate_FV.append(real_estate_FV_value)
                stocks_FV.append(stocks_FV_value)
                amount_FV_value = (real_estate_FV_value * (real_estate_swr / 100)) + (
                        stocks_FV_value * (stocks_swr / 100)
                )
                crypto_FV.append(int(current_goal * (crypto / 100)))
                commodities_FV.append(int(current_goal * (commodities / 100)))
                collectables_FV.append(int(current_goal * (collectables / 100)))
                cash_FV.append(int(current_goal * (cash / 100)))
                amount_FV.append(amount_FV_value)

            print(goals)
            retirementgoal.user = request.user
            form = RetirementGoalForm(instance=retirementgoal, user=request.user)

            if request.method == "POST":
                form = RetirementGoalForm(request.POST, instance=retirementgoal, user=request.user)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect("/retiregoals/")
            zipped = zip(
                years,
                goals,
                realstate_FV,
                stocks_FV,
                crypto_FV,
                commodities_FV,
                collectables_FV,
                cash_FV,
                amount_FV,
            )
            context = {
                "form": form,
                "current_year": str(current_year),
                "years": years,
                "adjusted_goal": str(adjusted_goal),
                "zipped": zipped,
            }

            return render(request, "retirementgoals/main.html", context)

    else:
        return render(request, "retirementgoals/main.html")
