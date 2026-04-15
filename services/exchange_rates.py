from decimal import Decimal
from dataclasses import dataclass


@dataclass
class ExchangeRates:
    dollar_blue: Decimal
    bitcoin: Decimal
    uva: Decimal


def get_current_exchange_rates() -> ExchangeRates:
    from services import (
        bluelytics_service,
        coingecko_service,
        bcra_service,
    )
    
    dollar_blue = Decimal('0')
    bitcoin = Decimal('0')
    uva = Decimal('0')
    
    blue_rate = bluelytics_service.get_blue_rate()
    if blue_rate:
        dollar_blue = Decimal(str(blue_rate.buy))
    
    btc_price = coingecko_service.get_bitcoin_price()
    if btc_price:
        bitcoin = Decimal(str(btc_price.price_ars))
    
    uva_data = bcra_service.get_uva_data()
    if uva_data:
        uva = Decimal(str(uva_data.uva_price))
    
    return ExchangeRates(
        dollar_blue=dollar_blue,
        bitcoin=bitcoin,
        uva=uva
    )
