"""
Módulo de cálculo de costo de oportunidad para ArsForte.

Calcula cuánto habría rendido el dinero del usuario si lo hubiera invertido
en lugar de mantenerlo en pesos. Compara con:
- Dólar blue
- Bitcoin
- Plazo Fijo UVA

También calcula la pérdida por inflación de mantener dinero en pesos.
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from services import (
    bluelytics_service,
    coingecko_service,
    inflation_service,
    bcra_service,
    historical_rates,
)


@dataclass
class OpportunityCost:
    """
    Representa el resultado del análisis de costo de oportunidad para una alternativa.
    
    Attributes:
        original_amount: Monto original de la transacción.
        current_value: Valor actual si se hubiera invertido en esta alternativa.
        gain_loss: Ganancia o pérdida en términos absolutos.
        percentage: Porcentaje de ganancia o pérdida.
        instrument: Nombre del instrumento alternativo.
        details: Detalles adicionales (precios entonces vs ahora).
    """
    original_amount: Decimal
    current_value: Decimal
    gain_loss: Decimal
    percentage: float
    instrument: str
    details: str


@dataclass
class TransactionAnalysis:
    """
    Resultado completo del análisis de costo de oportunidad de una transacción.
    
    Incluye el valor actual en pesos (considerando inflación) y la comparación
    con cada alternativa de inversión.
    
    Attributes:
        transaction_date: Fecha de la transacción.
        original_amount: Monto original.
        instrument: Instrumento de la transacción.
        value_in_pesos_today: Valor actual considerando inflación.
        inflation_loss: Pérdida por inflación.
        inflation_loss_pct: Porcentaje de pérdida por inflación.
        dollar_blue_value: Análisis vs dólar blue.
        bitcoin_value: Análisis vs Bitcoin.
        plazo_fijo_value: Análisis vs Plazo Fijo UVA.
    """
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
    """
    Calcula el costo de oportunidad entre dos momentos de tiempo.
    
    Fórmula:
        valor_actual = monto_original × (precio_actual / precio_entonces)
        ganancia_perdida = valor_actual - monto_original
    
    Args:
        original_amount: Monto de la transacción.
        start_rate: Cotización/precio del activo en la fecha de la transacción.
        current_rate: Cotización/precio actual del activo.
        instrument_name: Nombre del instrumento para mostrar.
        details: Detalles adicionales para mostrar al usuario.
    
    Returns:
        OpportunityCost con el análisis completo.
    """
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
    """
    Calcula la pérdida de poder adquisitivo por inflación.
    
    Fórmula:
        valor_actual = monto × (1 + tasa_mensual)^(-meses)
        pérdida = monto - valor_actual
    
    Args:
        amount: Monto a calcular la pérdida.
        months: Cantidad de meses transcurridos.
        monthly_rate: Tasa de inflación mensual (ej: 0.08 para 8%).
    
    Returns:
        Tupla con (valor_actual, porcentaje_pérdida).
    """
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
    instrument: str,
    exchange_rate_dollar_blue: Optional[Decimal] = None,
    exchange_rate_bitcoin: Optional[Decimal] = None,
    exchange_rate_uva: Optional[Decimal] = None
) -> TransactionAnalysis:
    """
    Analiza el costo de oportunidad de una transacción.
    
    Calcula cuánto habría rendido el monto si se hubiera invertido en alternativas
    (dólar blue, bitcoin, plazo fijo UVA) en lugar de mantenerlo en pesos.
    
    Args:
        amount: Monto de la transacción.
        transaction_date: Fecha de la transacción.
        instrument: Instrumento de la transacción ('pesos', 'dolar_blue', etc).
        exchange_rate_dollar_blue: Cotización del dólar blue en fecha de transacción.
        exchange_rate_bitcoin: Precio del bitcoin en fecha de transacción.
        exchange_rate_uva: Valor UVA en fecha de transacción.
    
    Returns:
        TransactionAnalysis con el análisis completo.
    
    Nota:
        Si los exchange rates de la transacción son None, no se puede calcular
        el costo de oportunidad (necesitamos saber cuánto valía el activo
        cuando se hizo la transacción).
    """
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
    
    # Calcula pérdida por inflación solo si está en pesos
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
    
    # Dólar Blue: cuánto hubiera ganado si compraba dólares
    # Fórmula: pesos / precio_dólar_entonces × precio_dólar_hoy
    # Si no hay rate histórico, usa el actual como aproximación
    dollar_blue_value = None
    if blue_rate and blue_rate.buy > 0:
        if exchange_rate_dollar_blue:
            start_rate = float(exchange_rate_dollar_blue)
            details = f'Dólar entonces: ${exchange_rate_dollar_blue:,.0f} → hoy: ${blue_rate.buy:,.0f}'
        else:
            start_rate = blue_rate.buy
            details = f'Dólar aprox: ${blue_rate.buy:,.0f} (sin datos históricos)'
        
        dollar_blue_value = calculate_opportunity_cost(
            original_amount=amount,
            start_rate=start_rate,
            current_rate=blue_rate.buy,
            instrument_name='Dólar Blue',
            details=details
        )
    
    # Bitcoin: cuánto hubiera ganado si compraba BTC
    # Fórmula: pesos / btc_entonces × btc_hoy
    bitcoin_value = None
    if bitcoin_price and bitcoin_price.price_ars > 0:
        if exchange_rate_bitcoin:
            start_rate = float(exchange_rate_bitcoin)
            details = f'BTC entonces: ${exchange_rate_bitcoin:,.0f} → hoy: ${bitcoin_price.price_ars:,.0f}'
        else:
            start_rate = bitcoin_price.price_ars
            details = f'BTC aprox: ${bitcoin_price.price_ars:,.0f} (sin datos históricos)'
        
        bitcoin_value = calculate_opportunity_cost(
            original_amount=amount,
            start_rate=start_rate,
            current_rate=bitcoin_price.price_ars,
            instrument_name='Bitcoin',
            details=details
        )
    
    # Plazo Fijo UVA: interés compuesto sobre UVAs
    # Fórmula: monto × (1 + tasa_mensual)^meses
    plazo_fijo_value = None
    if uva_data:
        monthly_rate = uva_data.nominal_rate / 12
        months_decimal = days_diff / 30
        current_value = amount * Decimal(str((1 + monthly_rate) ** months_decimal))
        gain_loss = current_value - amount
        percentage = (float(current_value) / float(amount) - 1) * 100
        
        if exchange_rate_uva:
            details = f'UVA entonces: ${exchange_rate_uva:,.0f} → hoy: ${uva_data.uva_price:,.0f}'
        else:
            details = f'UVA aprox: ${uva_data.uva_price:,.0f} (sin datos históricos)'
        
        plazo_fijo_value = OpportunityCost(
            original_amount=amount,
            current_value=current_value,
            gain_loss=gain_loss,
            percentage=percentage,
            instrument='Plazo Fijo UVA',
            details=details
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
    """
    Calcula el costo de oportunidad total del usuario para el mes.
    
    Usa la transacción más antigua del período para obtener los exchange rates
    de referencia y calcula cuánto habría ganado el balance total.
    
    Args:
        user: Usuario a analizar.
        month_start: Fecha de inicio del período (primer día del mes).
    
    Returns:
        Dict con totales de ingresos, gastos, balance y ganancias potenciales.
    """
    from transactions.models import Transaction, TransactionType
    
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
    
    # Calcula balance en pesos (neto de ingresos y gastos en pesos)
    pesos_income = sum(
        (tx.amount for tx in incomes if tx.instrument_type == 'pesos'),
        Decimal('0')
    )
    pesos_expense = sum(
        (tx.amount for tx in expenses if tx.instrument_type == 'pesos'),
        Decimal('0')
    )
    balance_in_pesos = max(pesos_income - pesos_expense, Decimal('0'))
    
    if balance <= 0:
        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
            'balance_in_pesos': balance_in_pesos,
            'potential_gain_dollar': Decimal('0'),
            'potential_gain_bitcoin': Decimal('0'),
            'potential_gain_uva': Decimal('0'),
        }
    
    from services.exchange_rates import get_current_exchange_rates
    current_rates = get_current_exchange_rates()
    
    total_dollar_gain = Decimal('0')
    total_bitcoin_gain = Decimal('0')
    total_uva_gain = Decimal('0')
    
    if current_rates.dollar_blue > 0:
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
        'balance_in_pesos': balance_in_pesos,
        'potential_gain_dollar': total_dollar_gain,
        'potential_gain_bitcoin': total_bitcoin_gain,
        'potential_gain_uva': total_uva_gain,
    }


def get_purchasing_power_analysis(
    user,
    start_date: date,
    end_date: date
) -> dict:
    """
    Analiza el poder adquisitivo del usuario desde start_date hasta end_date.

    Calcula:
    - Pérdida por inflación sobre ingresos en pesos
    - Ganancia potencial si hubiera dolarizado
    - Ganancia potencial si hubiera hecho Plazo Fijo UVA

    Args:
        user: Usuario a analizar.
        start_date: Fecha de inicio del período.
        end_date: Fecha de fin del período.

    Returns:
        Dict con análisis de poder adquisitivo.
    """
    from transactions.models import Transaction, TransactionType

    incomes = Transaction.objects.filter(
        user=user,
        date__gte=start_date,
        date__lte=end_date,
        transaction_type=TransactionType.INCOME
    )
    total_income = sum((tx.amount for tx in incomes), Decimal('0'))

    if total_income <= 0:
        return {
            'total_income': Decimal('0'),
            'start_date': start_date,
            'end_date': end_date,
            'inflation_loss_pct': 0.0,
            'inflation_loss_amount': Decimal('0'),
            'dollar_gain_pct': 0.0,
            'dollar_gain_amount': Decimal('0'),
            'uva_gain_pct': 0.0,
            'uva_gain_amount': Decimal('0'),
        }

    historical = historical_rates.historical_rates_service
    inflation = inflation_service.get_inflation()
    uva_data = bcra_service.get_uva_data()

    months_diff = max(1, (end_date - start_date).days / 30)

    start_blue = historical.get_blue_rate(start_date)
    current_blue = bluelytics_service.get_blue_rate()
    start_uva = historical.get_uva_rate(start_date)
    start_btc = historical.get_btc_price(start_date)
    current_btc = coingecko_service.get_bitcoin_price()

    inflation_loss_pct = 0.0
    inflation_loss_amount = Decimal('0')
    if inflation:
        inflation_loss_pct = ((1 + inflation.monthly_rate) ** months_diff - 1) * 100
        inflation_loss_amount = total_income * Decimal(str(inflation_loss_pct / 100))

    dollar_gain_pct = 0.0
    dollar_gain_amount = Decimal('0')
    if start_blue and current_blue and current_blue.buy > 0:
        start_rate = float(start_blue.value)
        current_rate = current_blue.buy
        if start_rate > 0:
            dollar_gain_pct = (current_rate / start_rate - 1) * 100
            dollar_gain_amount = total_income * Decimal(str(dollar_gain_pct / 100))

    uva_gain_pct = 0.0
    uva_gain_amount = Decimal('0')
    if start_uva and uva_data:
        start_uva_value = float(start_uva.value)
        current_uva_value = uva_data.uva_price
        monthly_rate = uva_data.nominal_rate / 12
        if start_uva_value > 0:
            theoretical_uva_gain = float(total_income) * ((1 + monthly_rate) ** months_diff - 1)
            actual_rate_change = (current_uva_value / start_uva_value - 1)
            uva_gain_pct = actual_rate_change * 100
            uva_gain_amount = Decimal(str(uva_gain_pct / 100)) * total_income

    return {
        'total_income': total_income,
        'start_date': start_date,
        'end_date': end_date,
        'inflation_loss_pct': round(inflation_loss_pct, 2),
        'inflation_loss_amount': abs(inflation_loss_amount),
        'dollar_gain_pct': round(dollar_gain_pct, 2),
        'dollar_gain_amount': max(dollar_gain_amount, Decimal('0')),
        'uva_gain_pct': round(uva_gain_pct, 2),
        'uva_gain_amount': max(uva_gain_amount, Decimal('0')),
    }
