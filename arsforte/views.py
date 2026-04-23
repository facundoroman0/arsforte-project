from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Sum
from decimal import Decimal
from datetime import date, timedelta
from transactions.models import Transaction, TransactionType, InstrumentType
from services import opportunity_cost, bluelytics_service, coingecko_service, bcra_service
from services.alerts import get_user_alerts
from services.api_status import get_apis_status


def get_year_start() -> date:
    today = date.today()
    return date(today.year, 1, 1)


def get_current_rates() -> dict:
    official_rate = bluelytics_service.get_official_rate()
    blue_rate = bluelytics_service.get_blue_rate()
    btc_price = coingecko_service.get_bitcoin_price()
    uva_data = bcra_service.get_uva_data()
    
    return {
        'dolar_oficial': Decimal(str(official_rate.sell)) if official_rate and official_rate.sell > 0 else Decimal('1000'),
        'dolar_blue': Decimal(str(blue_rate.sell)) if blue_rate and blue_rate.sell > 0 else Decimal('1000'),
        'bitcoin': Decimal(str(btc_price.price_ars)) if btc_price and btc_price.price_ars > 0 else Decimal('100000000'),
        'uva': Decimal(str(uva_data.uva_price)) if uva_data else Decimal('400'),
    }


def get_amount_in_ars(transaction: Transaction, rates: dict) -> Decimal:
    instrument = transaction.instrument_type
    
    if instrument == InstrumentType.PESOS:
        return transaction.amount
    
    if instrument == InstrumentType.DOLAR_OFICIAL:
        rate = transaction.exchange_rate_dolar_oficial or rates['dolar_oficial']
        return transaction.amount * rate
    
    if instrument == InstrumentType.DOLAR_BLUE:
        rate = transaction.exchange_rate_dollar_blue or rates['dolar_blue']
        return transaction.amount * rate
    
    if instrument == InstrumentType.BITCOIN:
        rate = transaction.exchange_rate_bitcoin or rates['bitcoin']
        return transaction.amount * rate
    
    if instrument == InstrumentType.PLAZO_FIJO_UVA:
        rate = transaction.exchange_rate_uva or rates['uva']
        return transaction.amount * rate
    
    return transaction.amount


def calculate_usd_values(incomes: Decimal, expenses: Decimal, balance: Decimal, rate: Decimal) -> dict:
    if rate > 0:
        return {
            'incomes_usd': round(incomes / rate, 2),
            'expenses_usd': round(expenses / rate, 2),
            'balance_usd': round(balance / rate, 2),
        }
    return {'incomes_usd': Decimal('0'), 'expenses_usd': Decimal('0'), 'balance_usd': Decimal('0')}


class DashboardView(LoginRequiredMixin, View):
    template_name = 'dashboard.html'
    login_url = 'login'

    def get(self, request):
        today = date.today()
        month_start = today.replace(day=1)
        year_start = get_year_start()
        
        transactions = Transaction.objects.filter(user=request.user)
        month_transactions = transactions.filter(date__gte=month_start, date__lte=today)
        rates = get_current_rates()
        
        incomes_list = [
            get_amount_in_ars(tx, rates) 
            for tx in month_transactions.filter(transaction_type=TransactionType.INCOME)
        ]
        incomes = sum(incomes_list, Decimal('0'))
        
        expenses_list = [
            get_amount_in_ars(tx, rates) 
            for tx in month_transactions.filter(transaction_type=TransactionType.EXPENSE)
        ]
        expenses = sum(expenses_list, Decimal('0'))
        
        balance = incomes - expenses
        
        last_day_prev = month_start - timedelta(days=1)
        first_day_prev = last_day_prev.replace(day=1)
        
        prev_month_transactions = transactions.filter(
            date__gte=first_day_prev,
            date__lt=month_start
        )
        
        prev_incomes_list = [
            get_amount_in_ars(tx, rates) 
            for tx in prev_month_transactions.filter(transaction_type=TransactionType.INCOME)
        ]
        prev_incomes = sum(prev_incomes_list, Decimal('0'))
        
        prev_expenses_list = [
            get_amount_in_ars(tx, rates) 
            for tx in prev_month_transactions.filter(transaction_type=TransactionType.EXPENSE)
        ]
        prev_expenses = sum(prev_expenses_list, Decimal('0'))
        
        prev_balance = prev_incomes - prev_expenses
        
        official_rate = bluelytics_service.get_official_rate()
        rate = Decimal(str(official_rate.sell)) if official_rate and official_rate.sell > 0 else Decimal('1000')
        
        usd_values = calculate_usd_values(incomes, expenses, balance, rate)
        
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
            'incomes_usd': usd_values['incomes_usd'],
            'expenses_usd': usd_values['expenses_usd'],
            'balance_usd': usd_values['balance_usd'],
            'current_rate': rate,
            'instrument_distribution': instrument_distribution,
            'recent_transactions': recent_transactions,
            'opportunity': opportunity,
            'purchasing_power': purchasing_power,
            'alerts': alerts,
            'apis_status': apis_status,
            'prev_month_incomes': prev_incomes,
            'prev_month_expenses': prev_expenses,
            'prev_month_balance': prev_balance,
            'prev_month_name': first_day_prev.strftime('%B'),
        }
        return render(request, self.template_name, context)
