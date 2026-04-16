"""
Tests para validar los cálculos de costo de oportunidad.
"""
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase
from services.opportunity_cost import (
    calculate_opportunity_cost,
    calculate_inflation_loss,
)


class CalculationTests(TestCase):
    """Tests para validar fórmulas de cálculo."""

    def test_calculate_opportunity_cost_dollar_gain(self):
        """Test: Si el dólar sube,应该有 ganancia."""
        result = calculate_opportunity_cost(
            original_amount=Decimal('120000'),
            start_rate=1200.0,
            current_rate=1350.0,
            instrument_name='Dólar Blue',
            details='Test'
        )
        
        self.assertEqual(result.original_amount, Decimal('120000'))
        self.assertEqual(result.current_value, Decimal('135000'))
        self.assertEqual(result.gain_loss, Decimal('15000'))
        self.assertGreater(result.percentage, 0)

    def test_calculate_opportunity_cost_dollar_loss(self):
        """Test: Si el dólar baja,应该有 pérdida."""
        result = calculate_opportunity_cost(
            original_amount=Decimal('120000'),
            start_rate=1200.0,
            current_rate=1100.0,
            instrument_name='Dólar Blue',
            details='Test'
        )
        
        self.assertAlmostEqual(float(result.current_value), 110000.0, places=0)
        self.assertLess(result.gain_loss, Decimal('0'))
        self.assertLess(result.percentage, 0)

    def test_calculate_opportunity_cost_zero_start_rate(self):
        """Test: Si start_rate es 0, deve volver el monto original."""
        result = calculate_opportunity_cost(
            original_amount=Decimal('100000'),
            start_rate=0.0,
            current_rate=1500.0,
            instrument_name='Dólar Blue',
            details='Test'
        )
        
        self.assertEqual(result.current_value, Decimal('100000'))
        self.assertEqual(result.gain_loss, Decimal('0'))
        self.assertEqual(result.percentage, 0.0)

    def test_calculate_opportunity_cost_no_change(self):
        """Test: Si las tasas no cambian,应该没有 gain/loss."""
        result = calculate_opportunity_cost(
            original_amount=Decimal('100000'),
            start_rate=1200.0,
            current_rate=1200.0,
            instrument_name='Dólar Blue',
            details='Test'
        )
        
        self.assertEqual(result.current_value, Decimal('100000'))
        self.assertEqual(result.gain_loss, Decimal('0'))
        self.assertEqual(result.percentage, 0.0)

    def test_calculate_inflation_loss(self):
        """Test: Pérdida por inflación mensual."""
        current_value, loss_pct = calculate_inflation_loss(
            amount=Decimal('100000'),
            months=1,
            monthly_rate=0.03
        )
        
        self.assertLess(current_value, Decimal('100000'))
        self.assertAlmostEqual(float(current_value), 97087.38, places=0)
        self.assertGreater(loss_pct, 0)

    def test_calculate_inflation_loss_multiple_months(self):
        """Test: Pérdida por inflación acumulada."""
        current_value, loss_pct = calculate_inflation_loss(
            amount=Decimal('100000'),
            months=6,
            monthly_rate=0.03
        )
        
        self.assertLess(current_value, Decimal('100000'))
        self.assertGreater(loss_pct, 10)

    def test_calculate_inflation_loss_zero_amount(self):
        """Test: Con monto 0, no hay pérdida."""
        current_value, loss_pct = calculate_inflation_loss(
            amount=Decimal('0'),
            months=1,
            monthly_rate=0.03
        )
        
        self.assertEqual(current_value, Decimal('0'))
        self.assertEqual(loss_pct, 0.0)

    def test_calculate_inflation_loss_zero_rate(self):
        """Test: Con tasa 0, no hay pérdida."""
        current_value, loss_pct = calculate_inflation_loss(
            amount=Decimal('100000'),
            months=1,
            monthly_rate=0.0
        )
        
        self.assertEqual(current_value, Decimal('100000'))
        self.assertEqual(loss_pct, 0.0)


class CalculationFormulaTests(TestCase):
    """Tests para verificar fórmulas específicas del PRD."""

    def test_dollar_blue_formula_from_prd(self):
        """
        Test: Verificar fórmula del PRD
        Transacción: $100,000 en pesos
        Dólar el 01/04: $1,200
        Dólar hoy: $1,350
        USD comprados: 83.33
        Valor hoy: $112,500
        Fórmula: $100,000 / $1,200 × $1,350 = $112,500
        """
        result = calculate_opportunity_cost(
            original_amount=Decimal('100000'),
            start_rate=1200.0,
            current_rate=1350.0,
            instrument_name='Dólar Blue',
            details='Test PRD'
        )
        
        expected_value = Decimal('100000') * Decimal('1350') / Decimal('1200')
        self.assertEqual(result.current_value, expected_value)
        self.assertAlmostEqual(float(result.current_value), 112500.0, places=0)

    def test_inflation_formula_simple(self):
        """
        Test: Verificar fórmula de inflación
        Fórmula: valor_actual = monto × (1 + tasa)^(-meses)
        """
        amount = Decimal('100000')
        monthly_rate = 0.08
        months = 1
        
        current_value, _ = calculate_inflation_loss(
            amount=amount,
            months=months,
            monthly_rate=monthly_rate
        )
        
        expected = amount * Decimal(str((1 + monthly_rate) ** (-months)))
        self.assertAlmostEqual(float(current_value), float(expected), places=2)
