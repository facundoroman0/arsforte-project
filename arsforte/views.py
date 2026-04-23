from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Sum
from decimal import Decimal
from datetime import date
from transactions.models import Transaction, TransactionType
from services import opportunity_cost
from services.alerts import get_user_alerts
from services.api_status import get_apis_status


def get_year_start() -> date:
    today = date.today()
    return date(today.year, 1, 1)


class DashboardView(LoginRequiredMixin, View):
    template_name = 'dashboard.html'
    login_url = 'login'

    def get(self, request):
        today = date.today()
        month_start = today.replace(day=1)
        year_start = get_year_start()
        
        transactions = Transaction.objects.filter(user=request.user)
        month_transactions = transactions.filter(date__gte=month_start)
        
        incomes = month_transactions.filter(
            transaction_type=TransactionType.INCOME
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        expenses = month_transactions.filter(
            transaction_type=TransactionType.EXPENSE
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        balance = incomes - expenses
        
        instrument_distribution = month_transactions.values(
            'instrument_type'
        ).annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        total_by_instrument = {}
        for item in instrument_distribution:
            total_by_instrument[item['instrument_type']] = item['total']
        
        recent_transactions = transactions.order_by('-date', '-created_at')[:5]
        
        opportunity = opportunity_cost.get_total_opportunity_cost(
            request.user, month_start
        )
        
        purchasing_power = opportunity_cost.get_purchasing_power_analysis(
            request.user, year_start, today
        )
        
        alerts = get_user_alerts(request.user)
        apis_status = get_apis_status()
        
        context = {
            'incomes': incomes,
            'expenses': expenses,
            'balance': balance,
            'instrument_distribution': instrument_distribution,
            'recent_transactions': recent_transactions,
            'opportunity': opportunity,
            'purchasing_power': purchasing_power,
            'alerts': alerts,
            'apis_status': apis_status,
        }
        return render(request, self.template_name, context)
