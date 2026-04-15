"""
Template filters para formateo de montos en formato argentino.
"""
from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def money(value, decimals=2):
    """
    Formatea un valor como monto en pesos argentinos.
    
    Uso: {{ value|money }} o {{ value|money:0 }}
    
    Ejemplo: 1234567.89 → $1.234.567,89
    """
    if value is None:
        return '$0,00'
    
    try:
        value = Decimal(str(value))
    except (ValueError, TypeError):
        return '$0,00'
    
    if decimals == 0:
        formatted = f'{int(value):,}'.replace(',', '.')
        return f'${formatted}'
    else:
        integer_part = int(value)
        decimal_part = abs(value - integer_part)
        formatted_int = f'{integer_part:,}'.replace(',', '.')
        if decimal_part > 0:
            decimal_str = f'{decimal_part:.2f}'[2:]
            return f'${formatted_int},{decimal_str}'
        else:
            return f'${formatted_int},00'
