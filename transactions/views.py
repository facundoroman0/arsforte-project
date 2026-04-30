from datetime import date

from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from datetime import date
from .models import Transaction, TransactionType, Category, InstrumentType
from .forms import TransactionForm


def invalidate_dashboard_cache(user_id: int):
    today = date.today()
    for month in range(today.month, today.month + 2):
        cache_key = f"dashboard:{user_id}:{today.year}:{month}"
        cache.delete(cache_key)
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
            invalidate_dashboard_cache(request.user.id)
            
            if hasattr(form, 'warning_message'):
                messages.warning(request, form.warning_message)
            else:
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
            updated_transaction = form.save()
            
            new_date = form.cleaned_data['date']
            if not transaction.exchange_rate_dollar_blue:
                from services.exchange_rates import get_current_exchange_rates
                rates = get_current_exchange_rates()
                updated_transaction.exchange_rate_dollar_blue = rates.dollar_blue
                updated_transaction.exchange_rate_bitcoin = rates.bitcoin
                updated_transaction.exchange_rate_uva = rates.uva
                updated_transaction.save(update_fields=[
                    'exchange_rate_dollar_blue',
                    'exchange_rate_bitcoin',
                    'exchange_rate_uva'
                ])
            
            invalidate_dashboard_cache(request.user.id)

            if hasattr(form, 'warning_message'):
                messages.warning(request, form.warning_message)
            else:
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
        invalidate_dashboard_cache(request.user.id)
        messages.success(request, 'Transacción eliminada correctamente')
        return redirect('transactions:list')


class TransactionDetailView(LoginRequiredMixin, View):
    """
    Vista para obtener el análisis de costo de oportunidad de una transacción.
    Retorna HTML renderizado para ser usado en un modal.
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
        
        context = {
            'transaction': {
                'id': str(transaction.pk),
                'amount': transaction.amount,
                'date': transaction.date.strftime('%d/%m/%Y'),
                'type': transaction.transaction_type,
                'category': transaction.get_category_display(),
                'instrument': transaction.get_instrument_type_display(),
                'description': transaction.description,
            },
            'analysis': {
                'original_amount': analysis.original_amount,
                'value_in_pesos_today': analysis.value_in_pesos_today,
                'inflation_loss': analysis.inflation_loss,
                'inflation_loss_pct': analysis.inflation_loss_pct,
                'days_passed': (date.today() - transaction.date).days,
            },
            'alternatives': {
                'dollar_blue': self._format_opportunity(analysis.dollar_blue_value),
                'bitcoin': self._format_opportunity(analysis.bitcoin_value),
                'plazo_fijo': self._format_opportunity(analysis.plazo_fijo_value),
            } if analysis.dollar_blue_value else None,
        }
        
        return render(request, 'transactions/detail_content.html', context)
    
    def _format_opportunity(self, opportunity):
        if opportunity is None:
            return None
        return {
            'instrument': opportunity.instrument,
            'original_amount': opportunity.original_amount,
            'current_value': opportunity.current_value,
            'gain_loss': opportunity.gain_loss,
            'percentage': opportunity.percentage,
            'details': opportunity.details,
        }
