import requests
from dataclasses import dataclass
from typing import Optional
from .cache import cached


@dataclass
class BlueRate:
    buy: float
    sell: float
    source: str


class BluelyticsService:
    BASE_URL = 'https://api.bluelytics.com.ar/v2'

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
        except Exception:
            pass
        return None


bluelytics_service = BluelyticsService()
