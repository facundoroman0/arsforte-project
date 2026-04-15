from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from typing import Optional
import math

from services import (
    bluelytics_service,
    coingecko_service,
    inflation_service,
    bcra_service,
)


@dataclass
class OpportunityCost:
    original_amount: Decimal
    current_value: Decimal
    gain_loss: Decimal
    percentage: float
    instrument: str
    details: str


@dataclass
class TransactionAnalysis:
    transaction_date: date
    original_amount: Decimal
    instrument: str
    
    value_in_pesos_today: Decimal
    inflation_loss: Decimal
    inflation_loss_pct: float
    
    dollar_blue_value: Optional[OpportunityCost]
    bitcoin_value: Optional[OpportunityCost]
    plazo_fijo_value: Optional[OpportunityCost]


def calculate_opportunity_cost(
    original_amount: Decimal,
    start_rate: float,
    current_rate: float,
    instrument_name: str,
    details: str
) -> OpportunityCost:
    if start_rate == 0:
        return OpportunityCost(
            original_amount=original_amount,
            current_value=original_amount,
            gain_loss=Decimal('0'),
            percentage=0.0,
            instrument=instrument_name,
            details=details
        )
    
    current_value = original_amount * Decimal(str(current_rate / start_rate))
    gain_loss = current_value - original_amount
    percentage = (float(current_value) / float(original_amount) - 1) * 100
    
    return OpportunityCost(
        original_amount=original_amount,
        current_value=current_value,
        gain_loss=gain_loss,
        percentage=percentage,
        instrument=instrument_name,
        details=details
    )


def calculate_inflation_loss(
    amount: Decimal,
    months: int,
    monthly_rate: float
) -> tuple[Decimal, float]:
    if amount == 0:
        return amount, 0.0
    if monthly_rate == 0:
        return amount, 0.0
    
    current_value = amount * Decimal(str((1 + monthly_rate) ** (-months)))
    loss = amount - current_value
    loss_pct = (float(loss) / float(amount)) * 100
    
    return current_value, loss_pct


def analyze_transaction(
    amount: Decimal,
    transaction_date: date,
    instrument: str
) -> TransactionAnalysis:
    if amount == 0:
        return TransactionAnalysis(
            transaction_date=transaction_date,
            original_amount=amount,
            instrument=instrument,
            value_in_pesos_today=amount,
            inflation_loss=Decimal('0'),
            inflation_loss_pct=0.0,
            dollar_blue_value=None,
            bitcoin_value=None,
            plazo_fijo_value=None
        )
    
    today = date.today()
    days_diff = (today - transaction_date).days
    months = max(1, days_diff // 30)
    
    blue_rate = bluelytics_service.get_blue_rate()
    bitcoin_price = coingecko_service.get_bitcoin_price()
    inflation = inflation_service.get_inflation()
    uva_data = bcra_service.get_uva_data()
    
    if instrument == 'pesos':
        value_in_pesos_today = amount
        if inflation:
            value_in_pesos_today, inflation_loss_pct = calculate_inflation_loss(
                amount, months, inflation.monthly_rate
            )
        else:
            value_in_pesos_today, inflation_loss_pct = calculate_inflation_loss(
                amount, months, 0.03
            )
    else:
        value_in_pesos_today = amount
        inflation_loss_pct = 0.0
    
    dollar_blue_value = None
    if blue_rate and blue_rate.buy > 0:
        dollar_blue_value = calculate_opportunity_cost(
            original_amount=amount,
            start_rate=1,
            current_rate=blue_rate.buy,
            instrument_name='Dólar Blue',
            details=f'Cotización actual: ${blue_rate.buy}'
        )
    
    bitcoin_value = None
    if bitcoin_price and bitcoin_price.price_ars > 0:
        bitcoin_value = calculate_opportunity_cost(
            original_amount=amount,
            start_rate=1,
            current_rate=bitcoin_price.price_ars,
            instrument_name='Bitcoin',
            details=f'Precio actual: ${bitcoin_price.price_ars:,.0f}'
        )
    
    plazo_fijo_value = None
    if uva_data:
        monthly_rate = uva_data.nominal_rate / 12
        current_value = amount * Decimal(str((1 + monthly_rate) ** months))
        gain_loss = current_value - amount
        percentage = (float(current_value) / float(amount) - 1) * 100
        
        plazo_fijo_value = OpportunityCost(
            original_amount=amount,
            current_value=current_value,
            gain_loss=gain_loss,
            percentage=percentage,
            instrument='Plazo Fijo UVA',
            details=f'Tasa: {uva_data.nominal_rate * 100}% anual'
        )
    
    inflation_loss = amount - value_in_pesos_today
    
    return TransactionAnalysis(
        transaction_date=transaction_date,
        original_amount=amount,
        instrument=instrument,
        value_in_pesos_today=value_in_pesos_today,
        inflation_loss=inflation_loss,
        inflation_loss_pct=inflation_loss_pct,
        dollar_blue_value=dollar_blue_value,
        bitcoin_value=bitcoin_value,
        plazo_fijo_value=plazo_fijo_value
    )


def get_total_opportunity_cost(user, month_start) -> dict:
    from transactions.models import Transaction, TransactionType
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
    
    total_income = sum((tx.amount for tx in incomes), Decimal('0'))
    total_expense = sum((tx.amount for tx in expenses), Decimal('0'))
    balance = total_income - total_expense
    
    if balance <= 0:
        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
            'potential_gain_dollar': Decimal('0'),
            'potential_gain_bitcoin': Decimal('0'),
            'potential_gain_uva': Decimal('0'),
        }
    
    from services.exchange_rates import get_current_exchange_rates
    current_rates = get_current_exchange_rates()
    
    total_dollar_gain = Decimal('0')
    total_bitcoin_gain = Decimal('0')
    total_uva_gain = Decimal('0')
    
    if current_rates.dollar_blue > 0 and current_rates.dollar_blue > 0:
        oldest_income = incomes.order_by('date').first()
        if oldest_income and oldest_income.exchange_rate_dollar_blue:
            old_rate = oldest_income.exchange_rate_dollar_blue
            new_rate = current_rates.dollar_blue
            total_dollar_gain = balance * (new_rate / old_rate - 1)
    
    if current_rates.bitcoin > 0:
        oldest_income = incomes.order_by('date').first()
        if oldest_income and oldest_income.exchange_rate_bitcoin:
            old_rate = oldest_income.exchange_rate_bitcoin
            new_rate = current_rates.bitcoin
            total_bitcoin_gain = balance * (new_rate / old_rate - 1)
    
    if current_rates.uva > 0:
        oldest_income = incomes.order_by('date').first()
        if oldest_income and oldest_income.exchange_rate_uva:
            old_rate = oldest_income.exchange_rate_uva
            new_rate = current_rates.uva
            total_uva_gain = balance * (new_rate / old_rate - 1)
    
    return {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'potential_gain_dollar': total_dollar_gain,
        'potential_gain_bitcoin': total_bitcoin_gain,
        'potential_gain_uva': total_uva_gain,
    }
