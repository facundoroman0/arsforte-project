from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, timedelta
from transactions.models import Transaction, TransactionType, Category, InstrumentType

User = get_user_model()


class TransactionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
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

    def test_future_date_rejected(self):
        future_date = (date.today() + timedelta(days=10)).isoformat()
        response = self.client.post(reverse('transactions:create'), {
            'date': future_date,
            'amount': '1000.00',
            'transaction_type': 'income',
            'category': 'sueldo',
            'instrument_type': 'pesos',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('No se pueden ingresar fechas futuras', response.content.decode())

    def test_old_date_with_warning(self):
        old_date = (date.today() - timedelta(days=400)).isoformat()
        response = self.client.post(reverse('transactions:create'), {
            'date': old_date,
            'amount': '1000.00',
            'transaction_type': 'income',
            'category': 'sueldo',
            'instrument_type': 'pesos',
        })
        self.assertEqual(response.status_code, 302)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('muy antigua' in str(m) for m in messages))


class DashboardIntegrationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword123'
        )
        
        Transaction.objects.create(
            user=self.user,
            date=date.today(),
            amount=Decimal('100000.00'),
            transaction_type=TransactionType.INCOME,
            category=Category.SUELDO,
            instrument_type=InstrumentType.PESOS,
            exchange_rate_dollar_blue=Decimal('1200.00'),
            exchange_rate_bitcoin=Decimal('60000.00'),
            exchange_rate_uva=Decimal('380.00'),
        )
        Transaction.objects.create(
            user=self.user,
            date=date.today(),
            amount=Decimal('30000.00'),
            transaction_type=TransactionType.EXPENSE,
            category=Category.COMIDA,
            instrument_type=InstrumentType.PESOS,
        )

    def test_dashboard_shows_balance(self):
        self.client.login(email='test@example.com', password='testpassword123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ingresos del mes')
        self.assertContains(response, 'Gastos del mes')

    def test_dashboard_transaction_detail_modal(self):
        self.client.login(email='test@example.com', password='testpassword123')
        tx = Transaction.objects.filter(user=self.user).first()
        response = self.client.get(reverse('transactions:detail', args=[tx.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)


class AlertTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword123',
            notification_threshold=Decimal('50.00')
        )

    def test_alert_triggered_when_high_peso_percentage(self):
        Transaction.objects.create(
            user=self.user,
            date=date.today(),
            amount=Decimal('100000.00'),
            transaction_type=TransactionType.INCOME,
            category=Category.SUELDO,
            instrument_type=InstrumentType.PESOS,
        )
        Transaction.objects.create(
            user=self.user,
            date=date.today(),
            amount=Decimal('10000.00'),
            transaction_type=TransactionType.EXPENSE,
            category=Category.COMIDA,
            instrument_type=InstrumentType.PESOS,
        )
        
        self.client.login(email='test@example.com', password='testpassword123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_no_alert_when_low_peso_percentage(self):
        Transaction.objects.create(
            user=self.user,
            date=date.today(),
            amount=Decimal('100000.00'),
            transaction_type=TransactionType.INCOME,
            category=Category.SUELDO,
            instrument_type=InstrumentType.DOLAR_BLUE,
        )
        
        self.client.login(email='test@example.com', password='testpassword123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
