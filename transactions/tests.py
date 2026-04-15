from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date
from transactions.models import Transaction, TransactionType, Category, InstrumentType

User = get_user_model()


class TransactionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123'
        )
        self.client.login(email='test@example.com', password='testpassword123')
        
        self.transaction = Transaction.objects.create(
            user=self.user,
            date=date.today(),
            amount=Decimal('10000.00'),
            transaction_type=TransactionType.INCOME,
            category=Category.SUELDO,
            instrument_type=InstrumentType.PESOS,
            description='Test transaction'
        )

    def test_transaction_list_page_loads(self):
        response = self.client.get(reverse('transactions:list'))
        self.assertEqual(response.status_code, 200)

    def test_transaction_create(self):
        response = self.client.post(reverse('transactions:create'), {
            'date': '2026-04-14',
            'amount': '5000.00',
            'transaction_type': 'expense',
            'category': 'comida',
            'instrument_type': 'pesos',
            'description': 'Test expense'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Transaction.objects.filter(description='Test expense').exists())

    def test_transaction_update(self):
        response = self.client.post(
            reverse('transactions:update', args=[self.transaction.pk]),
            {
                'date': '2026-04-14',
                'amount': '15000.00',
                'transaction_type': 'income',
                'category': 'sueldo',
                'instrument_type': 'pesos',
                'description': 'Updated'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.amount, Decimal('15000.00'))

    def test_transaction_delete(self):
        response = self.client.post(reverse('transactions:delete', args=[self.transaction.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Transaction.objects.filter(pk=self.transaction.pk).exists())

    def test_transaction_list_filters(self):
        response = self.client.get(f"{reverse('transactions:list')}?category=sueldo")
        self.assertEqual(response.status_code, 200)

    def test_transaction_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('transactions:list'))
        self.assertEqual(response.status_code, 302)
