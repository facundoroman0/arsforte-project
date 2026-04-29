from datetime import timedelta
from django import forms
from .models import Transaction, TransactionType, Category, InstrumentType


# class GlassTextInput(forms.TextInput):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('attrs', {})
#         kwargs['attrs'].setdefault('class', 'glass-input')
#         super().__init__(*args, **kwargs)


# class GlassNumberInput(forms.NumberInput):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('attrs', {})
#         kwargs['attrs'].setdefault('class', 'glass-input')
#         super().__init__(*args, **kwargs)


# class GlassDateInput(forms.DateInput):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('attrs', {})
#         kwargs['attrs'].setdefault('class', 'glass-input')
#         kwargs['attrs'].setdefault('type', 'date')
#         super().__init__(*args, **kwargs)


# class GlassTextarea(forms.Textarea):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('attrs', {})
#         kwargs['attrs'].setdefault('class', 'glass-input')
#         kwargs['attrs'].setdefault('rows', 3)
#         super().__init__(*args, **kwargs)


class TransactionForm(forms.ModelForm):
    transaction_type = forms.ChoiceField(
        choices=TransactionType.choices,
        widget=forms.RadioSelect(),#attrs={'class': 'glass-radio'}
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
        # widgets = {
        #     'date': GlassDateInput(),
        #     'amount': GlassNumberInput(attrs={'step': '0.01', 'min': '0'}),
        #     'description': GlassTextarea(),
        # }

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
