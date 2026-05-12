"""
Servicio para obtener datos de inflación desde Argentina Datos.
"""
import logging
import requests
from dataclasses import dataclass
from typing import Optional
from .cache import cached

logger = logging.getLogger(__name__)


@dataclass
class InflationData:
    monthly_rate: float
    annual_rate: float
    source: str


class InflationService:
    BASE_URL = 'https://api.argentinadatos.com/v1'
    DEFAULT_MONTHLY = 0.03
    DEFAULT_ANNUAL = 0.40

    @cached(ttl_seconds=86400)
    def get_inflation(self) -> Optional[InflationData]:
        try:
            response = requests.get(
                f'{self.BASE_URL}/finanzas/indices/inflacion',
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    latest = data[-1]
                    monthly_rate = float(latest.get('valor', 0)) / 100
                    annual_rate = monthly_rate * 12
                    return InflationData(
                        monthly_rate=monthly_rate,
                        annual_rate=annual_rate,
                        source='argentinadatos'
                    )
            else:
                logger.warning(
                    f'Inflation API returned status {response.status_code}'
                )
        except requests.Timeout:
            logger.error('Inflation API request timed out')
        except requests.ConnectionError as e:
            logger.error(f'Inflation API connection error: {e}')
        except Exception as e:
            logger.error(f'Inflation API unexpected error: {e}')
        return self._get_default_inflation()

    def _get_default_inflation(self) -> InflationData:
        return InflationData(
            monthly_rate=self.DEFAULT_MONTHLY,
            annual_rate=self.DEFAULT_ANNUAL,
            source='default'
        )


inflation_service = InflationService()
