from datetime import timedelta
from django import forms
from .models import Transaction, TransactionType, Category, InstrumentType


class TransactionForm(forms.ModelForm):
    transaction_type = forms.ChoiceField(
        choices=TransactionType.choices,
        widget=forms.RadioSelect,
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_date = None
        if self.instance and self.instance.pk:
            self.old_date = self.instance.date

    class Meta:
        model = Transaction
        fields = [
            'date', 'amount', 'transaction_type',
            'category', 'instrument_type', 'description'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if not date:
            return date
        
        today = date.today()
        
        if date > today:
            raise forms.ValidationError('No se pueden ingresar fechas futuras')
        
        one_year_ago = today - timedelta(days=365)
        if date < one_year_ago:
            self.warning_message = (
                f'La fecha seleccionada es muy antigua '
                f'({date.strftime("%d/%m/%Y")}). '
                f'No habrá datos históricos de cotizaciones para esta fecha.'
            )
        
        return date

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise forms.ValidationError('El monto debe ser mayor a 0')
        return amount
