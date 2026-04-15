from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'user', 'transaction_type', 'category', 'instrument_type', 'amount']
    list_filter = ['transaction_type', 'category', 'instrument_type']
    search_fields = ['user__email', 'description']
    date_hierarchy = 'date'
