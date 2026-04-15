import requests
from dataclasses import dataclass
from typing import Optional
from .cache import cached


@dataclass
class BitcoinPrice:
    price_ars: float
    price_usd: float
    source: str


class CoinGeckoService:
    BASE_URL = 'https://api.coingecko.com/api/v3'

    @cached(ttl_seconds=900)
    def get_bitcoin_price(self) -> Optional[BitcoinPrice]:
        try:
            response = requests.get(
                f'{self.BASE_URL}/simple/price',
                params={
                    'ids': 'bitcoin',
                    'vs_currencies': 'ars,usd'
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                btc = data.get('bitcoin', {})
                return BitcoinPrice(
                    price_ars=btc.get('ars', 0),
                    price_usd=btc.get('usd', 0),
                    source='coingecko'
                )
        except Exception:
            pass
        return None


coingecko_service = CoinGeckoService()
