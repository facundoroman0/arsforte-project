"""
Servicio para verificar el estado de las APIs externas.
"""
from dataclasses import dataclass
from typing import List

from . import bluelytics_service, coingecko_service, bcra_service, inflation_service


@dataclass
class APIStatus:
    name: str
    status: str
    source: str
    is_healthy: bool


def get_apis_status() -> List[APIStatus]:
    """
    Verifica el estado de todas las APIs externas.
    
    Returns:
        Lista de estados de cada API.
    """
    statuses = []
    
    blue_rate = bluelytics_service.get_blue_rate()
    statuses.append(APIStatus(
        name='Dólar Blue',
        status='OK' if blue_rate and blue_rate.buy > 0 else 'Error',
        source=blue_rate.source if blue_rate else 'N/A',
        is_healthy=blue_rate is not None and blue_rate.buy > 0
    ))
    
    btc_price = coingecko_service.get_bitcoin_price()
    statuses.append(APIStatus(
        name='Bitcoin',
        status='OK' if btc_price and btc_price.price_ars > 0 else 'Error',
        source=btc_price.source if btc_price else 'N/A',
        is_healthy=btc_price is not None and btc_price.price_ars > 0
    ))
    
    uva_data = bcra_service.get_uva_data()
    statuses.append(APIStatus(
        name='UVA',
        status='OK',
        source=uva_data.source if uva_data else 'N/A',
        is_healthy=uva_data is not None
    ))
    
    inflation = inflation_service.get_inflation()
    statuses.append(APIStatus(
        name='Inflación',
        status='OK',
        source=inflation.source if inflation else 'N/A',
        is_healthy=inflation is not None
    ))
    
    return statuses
