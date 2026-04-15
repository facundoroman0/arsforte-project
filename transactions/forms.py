from django import forms
from .models import Transaction, TransactionType, Category, InstrumentType


class TransactionForm(forms.ModelForm):
    transaction_type = forms.ChoiceField(
        choices=TransactionType.choices,
        widget=forms.RadioSelect,
        required=True
    )

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

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise forms.ValidationError('El monto debe ser mayor a 0')
        return amount
