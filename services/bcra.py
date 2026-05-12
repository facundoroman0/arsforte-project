"""
Servicio para obtener datos del UVA desde Argentina Datos.
"""
import logging
import requests
from dataclasses import dataclass
from typing import Optional
from .cache import cached

logger = logging.getLogger(__name__)


@dataclass
class UVAData:
    uva_price: float
    nominal_rate: float
    source: str


class BCRAService:
    BASE_URL = 'https://api.argentinadatos.com/v1'
    DEFAULT_PRICE = 390.0
    DEFAULT_RATE = 0.03

    @cached(ttl_seconds=900)
    def get_uva_data(self) -> Optional[UVAData]:
        try:
            response = requests.get(
                f'{self.BASE_URL}/finanzas/indices/uva',
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    latest = data[-1]
                    uva_price = float(latest.get('valor', self.DEFAULT_PRICE))
                    return UVAData(
                        uva_price=uva_price,
                        nominal_rate=self.DEFAULT_RATE,
                        source='argentinadatos'
                    )
            else:
                logger.warning(f'UVA API returned status {response.status_code}')
        except requests.Timeout:
            logger.error('UVA API request timed out')
        except requests.ConnectionError as e:
            logger.error(f'UVA API connection error: {e}')
        except Exception as e:
            logger.error(f'UVA API unexpected error: {e}')
        return self._get_default_uva()

    def _get_default_uva(self) -> UVAData:
        return UVAData(
            uva_price=self.DEFAULT_PRICE,
            nominal_rate=self.DEFAULT_RATE,
            source='default'
        )


bcra_service = BCRAService()
