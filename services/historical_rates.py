"""
Servicio para obtener cotizaciones históricas desde APIs externas.

Proporciona datos históricos de:
- Dólar Blue (Bluelytics: evolution.json desde 2007)
- UVA (BCRA Monetarias v4.0: desde 2016)
- Bitcoin (CoinGecko: market_chart/range)
"""
import logging
import requests
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from functools import lru_cache

logger = logging.getLogger(__name__)


@dataclass
class HistoricalRate:
    value: Decimal
    date: date
    source: str


class HistoricalRatesService:
    CACHE_TTL = 3600
    UVA_ID = 31
    UVA_RATE_ID = 1227

    _blue_evolution: Optional[list[dict]] = None
    _blue_loaded: bool = False
    _uva_history: Optional[list[dict]] = None
    _uva_loaded: bool = False
    _uva_rate_history: Optional[list[dict]] = None
    _uva_rate_loaded: bool = False

    def get_blue_rate(self, target_date: date) -> Optional[HistoricalRate]:
        evolution = self._get_blue_evolution()
        if not evolution:
            return None

        closest = self._find_closest_date(evolution, target_date)
        if closest:
            return HistoricalRate(
                value=Decimal(str(closest['value_sell'])),
                date=date.fromisoformat(closest['date']),
                source='bluelytics'
            )
        return None

    def _get_blue_evolution(self) -> Optional[list[dict]]:
        if self._blue_loaded:
            return self._blue_evolution

        try:
            response = requests.get(
                'https://api.bluelytics.com.ar/v2/evolution.json',
                timeout=15
            )
            if response.status_code == 200:
                self._blue_evolution = response.json()
                self._blue_loaded = True
                return self._blue_evolution
        except Exception as e:
            logger.error(f'Bluelytics evolution API error: {e}')
        return None

    def get_uva_rate(self, target_date: date) -> Optional[HistoricalRate]:
        history = self._get_uva_history()
        if not history:
            return None

        filtered = [h for h in history if date.fromisoformat(h['fecha']) <= target_date]
        if filtered:
            latest = filtered[-1]
            return HistoricalRate(
                value=Decimal(str(latest['valor'])),
                date=date.fromisoformat(latest['fecha']),
                source='bcra'
            )
        return None

    def _get_uva_history(self) -> Optional[list[dict]]:
        if self._uva_loaded:
            return self._uva_history

        try:
            response = requests.get(
                f'https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/{self.UVA_ID}',
                params={'desde': '2016-01-01'},
                headers={'Accept': 'application/json'},
                timeout=15
            )
            if response.status_code == 200:
                data = response.json()
                self._uva_history = data.get('results', [{}])[0].get('detalle', [])
                self._uva_loaded = True
                return self._uva_history
        except Exception as e:
            logger.error(f'BCRA UVA API error: {e}')
        return None

    def get_uva_rate_history(self, target_date: date) -> Optional[HistoricalRate]:
        history = self._get_uva_rate_history()
        if not history:
            return None

        filtered = [h for h in history if date.fromisoformat(h['fecha']) <= target_date]
        if filtered:
            latest = filtered[-1]
            return HistoricalRate(
                value=Decimal(str(latest['valor'])),
                date=date.fromisoformat(latest['fecha']),
                source='bcra'
            )
        return None

    def _get_uva_rate_history(self) -> Optional[list[dict]]:
        if self._uva_rate_loaded:
            return self._uva_rate_history

        try:
            response = requests.get(
                f'https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/{self.UVA_RATE_ID}',
                params={'desde': '2016-01-01'},
                headers={'Accept': 'application/json'},
                timeout=15
            )
            if response.status_code == 200:
                data = response.json()
                self._uva_rate_history = data.get('results', [{}])[0].get('detalle', [])
                self._uva_rate_loaded = True
                return self._uva_rate_history
        except Exception as e:
            logger.error(f'BCRA UVA rate API error: {e}')
        return None

    def get_btc_price(self, target_date: date) -> Optional[HistoricalRate]:
        try:
            from_timestamp = int(datetime.combine(target_date, datetime.min.time()).timestamp())
            to_timestamp = int(datetime.combine(target_date, datetime.max.time()).timestamp())

            response = requests.get(
                'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range',
                params={
                    'vs_currency': 'ars',
                    'from': from_timestamp,
                    'to': to_timestamp,
                },
                timeout=15
            )

            if response.status_code == 200:
                data = response.json()
                prices = data.get('prices', [])
                if prices:
                    avg_price = sum(p[1] for p in prices) / len(prices)
                    return HistoricalRate(
                        value=Decimal(str(round(avg_price, 2))),
                        date=target_date,
                        source='coingecko'
                    )
            else:
                logger.warning(f'CoinGecko historical API status: {response.status_code}')
        except Exception as e:
            logger.error(f'CoinGecko historical API error: {e}')
        return None

    def _find_closest_date(
        self,
        data: list[dict],
        target_date: date,
        prefer_before: bool = True
    ) -> Optional[dict]:
        target_str = target_date.isoformat()
        closest_before = None
        closest_after = None

        for entry in data:
            entry_date = entry.get('date', '')
            if not entry_date:
                continue

            try:
                entry_date_obj = date.fromisoformat(entry_date)
                closest_before_date = (
                    date.fromisoformat(closest_before['date']) 
                    if closest_before else None
                )
                if entry_date_obj <= target_date:
                    if closest_before_date is None or entry_date_obj > closest_before_date:
                        closest_before = entry
                elif closest_after is None or entry_date_obj < date.fromisoformat(closest_after['date']):
                    closest_after = entry
            except ValueError:
                continue

        if prefer_before and closest_before:
            return closest_before
        if closest_after:
            return closest_after
        return closest_before


historical_rates_service = HistoricalRatesService()