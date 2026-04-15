import requests
from dataclasses import dataclass
from typing import Optional
from .cache import cached


@dataclass
class UVAData:
    uva_price: float
    nominal_rate: float
    source: str


class BCRAService:
    BASE_URL = 'https://api.bcra.gob.ar/api/v1'

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
                    uva_price=data.get('valor', 0),
                    nominal_rate=0.03,
                    source='bcra'
                )
        except Exception:
            pass
        return self._get_default_uva()

    def _get_default_uva(self) -> UVAData:
        return UVAData(
            uva_price=390.0,
            nominal_rate=0.03,
            source='default'
        )


bcra_service = BCRAService()
