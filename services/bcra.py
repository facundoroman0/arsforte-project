"""
Servicio para obtener datos del UVA desde el BCRA.
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
    BASE_URL = 'https://api.bcra.gob.ar/api/v1'
    DEFAULT_PRICE = 390.0
    DEFAULT_RATE = 0.03

    @cached(ttl_seconds=900)
    def get_uva_data(self) -> Optional[UVAData]:
        try:
            response = requests.get(
                f'{self.BASE_URL}/uvas',
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return UVAData(
                    uva_price=data.get('valor', self.DEFAULT_PRICE),
                    nominal_rate=self.DEFAULT_RATE,
                    source='bcra'
                )
            else:
                logger.warning(f'BCRA API returned status {response.status_code}')
        except requests.Timeout:
            logger.error('BCRA API request timed out')
        except requests.ConnectionError as e:
            logger.error(f'BCRA API connection error: {e}')
        except Exception as e:
            logger.error(f'BCRA API unexpected error: {e}')
        return self._get_default_uva()

    def _get_default_uva(self) -> UVAData:
        return UVAData(
            uva_price=self.DEFAULT_PRICE,
            nominal_rate=self.DEFAULT_RATE,
            source='default'
        )


bcra_service = BCRAService()
