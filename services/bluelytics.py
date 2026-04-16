"""
Servicio para obtener la cotización del dólar blue desde Bluelytics.
"""
import logging
import requests
from dataclasses import dataclass
from typing import Optional
from .cache import cached

logger = logging.getLogger(__name__)


@dataclass
class BlueRate:
    buy: float
    sell: float
    source: str
    is_stale: bool = False


class BluelyticsService:
    BASE_URL = 'https://api.bluelytics.com.ar/v2'
    DEFAULT_BUY = 0.0
    DEFAULT_SELL = 0.0

    @cached(ttl_seconds=900)
    def get_blue_rate(self) -> Optional[BlueRate]:
        try:
            response = requests.get(
                f'{self.BASE_URL}/latest',
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return BlueRate(
                    buy=data.get('blue', {}).get('value_buy', 0),
                    sell=data.get('blue', {}).get('value_sell', 0),
                    source='bluelytics'
                )
            else:
                logger.warning(
                    f'Bluelytics API returned status {response.status_code}'
                )
        except requests.Timeout:
            logger.error('Bluelytics API request timed out')
        except requests.ConnectionError as e:
            logger.error(f'Bluelytics API connection error: {e}')
        except Exception as e:
            logger.error(f'Bluelytics API unexpected error: {e}')
        return None


bluelytics_service = BluelyticsService()
