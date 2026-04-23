from decimal import Decimal
from dataclasses import dataclass
from transactions.models import InstrumentType


@dataclass
class ExchangeRates:
    dolar_oficial: Decimal
    dollar_blue: Decimal
    bitcoin: Decimal
    uva: Decimal


def get_current_exchange_rates() -> ExchangeRates:
    from services import (
        bluelytics_service,
        coingecko_service,
        bcra_service,
    )
    
    oficial_rate = bluelytics_service.get_official_rate()
    blue_rate = bluelytics_service.get_blue_rate()
    btc_price = coingecko_service.get_bitcoin_price()
    uva_data = bcra_service.get_uva_data()
    
    return ExchangeRates(
        dolar_oficial=Decimal(str(oficial_rate.sell)) if oficial_rate and oficial_rate.sell > 0 else Decimal('1000'),
        dollar_blue=Decimal(str(blue_rate.sell)) if blue_rate and blue_rate.sell > 0 else Decimal('1000'),
        bitcoin=Decimal(str(btc_price.price_ars)) if btc_price and btc_price.price_ars > 0 else Decimal('100000000'),
        uva=Decimal(str(uva_data.uva_price)) if uva_data else Decimal('400'),
    )


def get_amount_in_ars(transaction, rates: ExchangeRates) -> Decimal:
    instrument = transaction.instrument_type
    
    if instrument == InstrumentType.PESOS:
        return transaction.amount
    
    if instrument == InstrumentType.DOLAR_OFICIAL:
        rate = transaction.exchange_rate_dolar_oficial or rates.dolar_oficial
        return transaction.amount * rate
    
    if instrument == InstrumentType.DOLAR_BLUE:
        rate = transaction.exchange_rate_dollar_blue or rates.dollar_blue
        return transaction.amount * rate
    
    if instrument == InstrumentType.BITCOIN:
        rate = transaction.exchange_rate_bitcoin or rates.bitcoin
        return transaction.amount * rate
    
    if instrument == InstrumentType.PLAZO_FIJO_UVA:
        rate = transaction.exchange_rate_uva or rates.uva
        return transaction.amount * rate
    
    return transaction.amount
