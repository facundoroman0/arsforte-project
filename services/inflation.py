import requests
from dataclasses import dataclass
from typing import Optional
from .cache import cached


@dataclass
class InflationData:
    monthly_rate: float
    annual_rate: float
    source: str


class InflationService:
    BASE_URL = 'https://api.argentinadatos.com/v1'

    @cached(ttl_seconds=86400)
    def get_inflation(self) -> Optional[InflationData]:
        try:
            response = requests.get(
                f'{self.BASE_URL}/inflacion',
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return InflationData(
                    monthly_rate=data.get('mensual', 0) / 100,
                    annual_rate=data.get('anual', 0) / 100,
                    source='argentinadatos'
                )
        except Exception:
            pass
        return self._get_default_inflation()

    def _get_default_inflation(self) -> InflationData:
        return InflationData(
            monthly_rate=0.03,
            annual_rate=0.40,
            source='default'
        )


inflation_service = InflationService()
