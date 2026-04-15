"""
Módulo de alertas para FinZap.

Genera alertas para notificar al usuario sobre riesgos en su distribución
de instrumentos financieros.

Alertas generadas:
- Porcentaje de balance en pesos vs umbral configurable (PRD #27)
"""

from decimal import Decimal
from datetime import date
from typing import List
from dataclasses import dataclass

from django.db.models import Sum
from transactions.models import Transaction, TransactionType


@dataclass
class Alert:
    """
    Representa una alerta para el usuario.
    
    Attributes:
        type: Tipo de alerta ('warning', 'info', 'error').
        message: Mensaje descriptivo para mostrar al usuario.
        priority: Prioridad de la alerta ('low', 'medium', 'high').
    """
    type: str
    message: str
    priority: str


def check_peso_percentage(user, month_start) -> Alert | None:
    """
    Verifica si el porcentaje del balance en pesos supera el umbral configurado.
    
    Calcula qué porcentaje del dinero disponible (balance = ingresos - gastos)
    está mantenido en pesos. Si supera el umbral del usuario, genera una alerta.
    
    Args:
        user: Usuario autenticado con su umbral de notificación.
        month_start: Fecha de inicio del período a evaluar (primer día del mes).
    
    Returns:
        Alert si el porcentaje en pesos supera el umbral, None en caso contrario.
    
    Lógica:
        1. Obtiene ingresos y gastos del mes actual.
        2. Calcula el balance disponible.
        3. Suma los ingresos en pesos y resta los gastos en pesos para obtener
           cuánto del balance está efectivamente en pesos.
        4. Compara el porcentaje con el umbral del usuario.
    """
    # Obtiene todos los ingresos del mes para el usuario
    incomes = Transaction.objects.filter(
        user=user,
        date__gte=month_start,
        transaction_type=TransactionType.INCOME
    )
    
    # Obtiene todos los gastos del mes para el usuario
    expenses = Transaction.objects.filter(
        user=user,
        date__gte=month_start,
        transaction_type=TransactionType.EXPENSE
    )
    
    # Calcula totales usando agregación para eficiencia
    total_income = incomes.aggregate(total=Sum('amount'))['total'] or Decimal('0')
    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0')
    balance = total_income - total_expense
    
    # No hay alerta si no hay balance disponible
    if balance <= 0:
        return None
    
    # Suma ingresos que están en pesos
    pesos_income = incomes.filter(
        instrument_type='pesos'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    # Suma gastos que están en pesos
    pesos_expense = expenses.filter(
        instrument_type='pesos'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    # Balance en pesos = ingresos en pesos - gastos en pesos
    # Puede ser 0 si gastó todo lo que tenía en pesos
    pesos_balance = pesos_income - pesos_expense
    if pesos_balance < 0:
        pesos_balance = Decimal('0')
    
    # Porcentaje del balance que está en pesos
    pesos_percentage = (pesos_balance / balance) * 100
    
    # Genera alerta si supera el umbral configurable del usuario
    if pesos_percentage > float(user.notification_threshold):
        return Alert(
            type='warning',
            message=f'{pesos_percentage:.0f}% de tu balance está en pesos. Superaste el umbral de {user.notification_threshold:.0f}%.',
            priority='medium'
        )
    
    return None


def get_user_alerts(user) -> List[Alert]:
    """
    Genera todas las alertas activas para un usuario.
    
    Recopila y retorna una lista con todas las alertas que aplican
    al usuario basándose en su actividad del mes actual.
    
    Args:
        user: Usuario autenticado.
    
    Returns:
        Lista de objetos Alert activos para el usuario.
    """
    alerts = []
    today = date.today()
    # Primer día del mes actual para analizar el período en curso
    month_start = today.replace(day=1)
    
    # Verifica alerta de porcentaje en pesos
    peso_alert = check_peso_percentage(user, month_start)
    if peso_alert:
        alerts.append(peso_alert)
    
    return alerts
