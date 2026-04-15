from decimal import Decimal
from datetime import date
from typing import List
from dataclasses import dataclass

from django.db.models import Sum
from transactions.models import Transaction, TransactionType


@dataclass
class Alert:
    type: str
    message: str
    priority: str


def check_peso_percentage(user, month_start) -> Alert | None:
    from django.db.models import Sum
    
    incomes = Transaction.objects.filter(
        user=user,
        date__gte=month_start,
        transaction_type=TransactionType.INCOME
    )
    
    expenses = Transaction.objects.filter(
        user=user,
        date__gte=month_start,
        transaction_type=TransactionType.EXPENSE
    )
    
    total_income = incomes.aggregate(total=Sum('amount'))['total'] or Decimal('0')
    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0')
    balance = total_income - total_expense
    
    if total_income == 0:
        return None
    
    pesos_income = incomes.filter(
        instrument_type='pesos'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    pesos_percentage = (pesos_income / total_income) * 100
    
    message_parts = []
    message_parts.append(f'{pesos_percentage:.0f}% de tus ingresos están en pesos')
    
    if balance > 0:
        pesos_balance = pesos_income - total_expense
        if pesos_balance < 0:
            pesos_balance = Decimal('0')
        balance_percentage = (pesos_balance / balance) * 100 if balance > 0 else Decimal('0')
        message_parts.append(f'Disponés de ${balance} para invertir, {balance_percentage:.0f}% está en pesos')
    
    if pesos_percentage > float(user.notification_threshold):
        full_message = '. '.join(message_parts)
        return Alert(
            type='warning',
            message=full_message,
            priority='medium'
        )
    
    return None


def get_user_alerts(user) -> List[Alert]:
    alerts = []
    today = date.today()
    month_start = today.replace(day=1)
    
    peso_alert = check_peso_percentage(user, month_start)
    if peso_alert:
        alerts.append(peso_alert)
    
    return alerts
