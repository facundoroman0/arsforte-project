from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TransactionType(models.TextChoices):
    INCOME = 'income', 'Ingreso'
    EXPENSE = 'expense', 'Gasto'


class Category(models.TextChoices):
    SUELDO = 'sueldo', 'Sueldo'
    ALQUILER = 'alquiler', 'Alquiler'
    COMIDA = 'comida', 'Comida'
    TRANSPORTE = 'transporte', 'Transporte'
    ENTRETENIMIENTO = 'entretenimiento', 'Entretenimiento'
    SERVICIOS = 'servicios', 'Servicios'
    INVERSION = 'inversion', 'Inversión'
    AHORRO = 'ahorro', 'Ahorro'
    OTRO = 'otro', 'Otro'


class InstrumentType(models.TextChoices):
    PESOS = 'pesos', 'Pesos'
    DOLAR_OFICIAL = 'dolar_oficial', 'Dólar Oficial'
    DOLAR_BLUE = 'dolar_blue', 'Dólar Blue'
    PLAZO_FIJO_UVA = 'plazo_fijo_uva', 'Plazo Fijo UVA'
    BITCOIN = 'bitcoin', 'Bitcoin'


class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices
    )
    category = models.CharField(
        max_length=50,
        choices=Category.choices
    )
    instrument_type = models.CharField(
        max_length=30,
        choices=InstrumentType.choices
    )
    description = models.TextField(blank=True)
    
    exchange_rate_dollar_blue = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True,
        help_text="Cotización del dólar blue al momento de la transacción"
    )
    exchange_rate_dolar_oficial = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True,
        help_text="Cotización del dólar oficial al momento de la transacción"
    )
    exchange_rate_bitcoin = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True,
        help_text="Precio del Bitcoin (ARS) al momento de la transacción"
    )
    exchange_rate_uva = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True,
        help_text="Valor UVA al momento de la transacción"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['user', 'category']),
            models.Index(fields=['user', 'instrument_type']),
        ]

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.date}"
