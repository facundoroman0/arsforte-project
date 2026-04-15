from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Transaction, Category, InstrumentType
from .forms import TransactionForm
from services.opportunity_cost import analyze_transaction


class TransactionListView(LoginRequiredMixin, View):
    template_name = 'transactions/list.html'
    login_url = 'login'

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        
        category = request.GET.get('category')
        instrument = request.GET.get('instrument')
        search = request.GET.get('search')
        
        if category:
            transactions = transactions.filter(category=category)
        if instrument:
            transactions = transactions.filter(instrument_type=instrument)
        if search:
            transactions = transactions.filter(
                Q(description__icontains=search) | Q(category__icontains=search)
            )
        
        context = {
            'transactions': transactions,
            'categories': Category.choices,
            'instruments': InstrumentType.choices,
            'filter_category': category,
            'filter_instrument': instrument,
            'search': search,
        }
        return render(request, self.template_name, context)


class TransactionCreateView(LoginRequiredMixin, View):
    template_name = 'transactions/form.html'
    login_url = 'login'

    def get(self, request):
        form = TransactionForm()
        context = {'form': form, 'action': 'Crear'}
        return render(request, self.template_name, context)

    def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            
            from services.exchange_rates import get_current_exchange_rates
            rates = get_current_exchange_rates()
            transaction.exchange_rate_dollar_blue = rates.dollar_blue
            transaction.exchange_rate_bitcoin = rates.bitcoin
            transaction.exchange_rate_uva = rates.uva
            
            transaction.save()
            messages.success(request, 'Transacción creada correctamente')
            return redirect('transactions:list')
        context = {'form': form, 'action': 'Crear'}
        return render(request, self.template_name, context)


class TransactionUpdateView(LoginRequiredMixin, View):
    template_name = 'transactions/form.html'
    login_url = 'login'

    def get(self, request, pk):
        transaction = get_object_or_404(
            Transaction, pk=pk, user=request.user
        )
        form = TransactionForm(instance=transaction)
        context = {'form': form, 'action': 'Editar', 'transaction': transaction}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        transaction = get_object_or_404(
            Transaction, pk=pk, user=request.user
        )
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transacción actualizada correctamente')
            return redirect('transactions:list')
        context = {'form': form, 'action': 'Editar', 'transaction': transaction}
        return render(request, self.template_name, context)


class TransactionDeleteView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, pk):
        transaction = get_object_or_404(
            Transaction, pk=pk, user=request.user
        )
        transaction.delete()
        messages.success(request, 'Transacción eliminada correctamente')
        return redirect('transactions:list')


class TransactionDetailView(LoginRequiredMixin, View):
    """
    Vista para obtener el análisis de costo de oportunidad de una transacción.
    Retorna JSON para ser usado en un modal.
    """
    login_url = 'login'

    def get(self, request, pk):
        transaction = get_object_or_404(
            Transaction, pk=pk, user=request.user
        )
        
        analysis = analyze_transaction(
            amount=transaction.amount,
            transaction_date=transaction.date,
            instrument=transaction.instrument_type,
            exchange_rate_dollar_blue=transaction.exchange_rate_dollar_blue,
            exchange_rate_bitcoin=transaction.exchange_rate_bitcoin,
            exchange_rate_uva=transaction.exchange_rate_uva
        )
        
        data = {
            'transaction': {
                'id': str(transaction.pk),
                'amount': str(transaction.amount),
                'date': transaction.date.isoformat(),
                'type': transaction.transaction_type,
                'category': transaction.get_category_display(),
                'instrument': transaction.get_instrument_type_display(),
                'description': transaction.description,
            },
            'analysis': {
                'original_amount': str(analysis.original_amount),
                'value_in_pesos_today': str(analysis.value_in_pesos_today),
                'inflation_loss': str(analysis.inflation_loss),
                'inflation_loss_pct': analysis.inflation_loss_pct,
                'days_passed': (transaction.date.today() - transaction.date).days,
            },
            'alternatives': {
                'dollar_blue': self._format_opportunity(analysis.dollar_blue_value),
                'bitcoin': self._format_opportunity(analysis.bitcoin_value),
                'plazo_fijo': self._format_opportunity(analysis.plazo_fijo_value),
            } if analysis.dollar_blue_value else None,
        }
        
        return JsonResponse(data)
    
    def _format_opportunity(self, opportunity):
        if opportunity is None:
            return None
        return {
            'instrument': opportunity.instrument,
            'original_amount': str(opportunity.original_amount),
            'current_value': str(opportunity.current_value),
            'gain_loss': str(opportunity.gain_loss),
            'percentage': opportunity.percentage,
            'details': opportunity.details,
        }
