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
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Optional

from django.core.cache import cache

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
    REQUEST_TIMEOUT = 10

    HEADERS = {
        'Accept': 'application/json',
        'User-Agent': 'ArsForte/1.0 (https://github.com/arsforte)'
    }

    def _get_cache_key(self, prefix: str) -> str:
        return f'historical_rates:{prefix}'

    def _get_cached_data(self, prefix: str) -> Optional[list[dict]]:
        return cache.get(self._get_cache_key(prefix))

    def _set_cached_data(self, prefix: str, data: list[dict], ttl: int = None) -> None:
        cache.set(
            self._get_cache_key(prefix),
            data,
            ttl or self.CACHE_TTL
        )

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
        cached_data = self._get_cached_data('blue_evolution')
        if cached_data is not None:
            return cached_data

        try:
            response = requests.get(
                'https://api.bluelytics.com.ar/v2/evolution.json',
                timeout=self.REQUEST_TIMEOUT,
                headers=self.HEADERS
            )

            if response.status_code == 429:
                logger.warning('Bluelytics rate limit exceeded')
                return None

            if response.status_code == 200:
                data = response.json()
                one_year_ago = date.today() - timedelta(days=365)
                filtered_data = [
                    entry for entry in data
                    if entry.get('date', '') and date.fromisoformat(entry['date']) >= one_year_ago
                ]
                self._set_cached_data('blue_evolution', filtered_data)
                return filtered_data

            logger.warning(f'Bluelytics evolution API status: {response.status_code}')

        except requests.Timeout:
            logger.error('Bluelytics evolution API request timed out')
        except requests.ConnectionError as e:
            logger.error(f'Bluelytics evolution API connection error: {e}')
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
        cached_data = self._get_cached_data('uva_history')
        if cached_data is not None:
            return cached_data

        try:
            one_year_ago = (date.today() - timedelta(days=365)).isoformat()
            response = requests.get(
                f'https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/{self.UVA_ID}',
                params={'desde': one_year_ago},
                headers=self.HEADERS,
                timeout=self.REQUEST_TIMEOUT
            )

            if response.status_code == 429:
                logger.warning('BCRA rate limit exceeded')
                return None

            if response.status_code == 200:
                data = response.json()
                history = data.get('results', [{}])[0].get('detalle', [])
                self._set_cached_data('uva_history', history)
                return history

            logger.warning(f'BCRA UVA API status: {response.status_code}')

        except requests.Timeout:
            logger.error('BCRA UVA API request timed out')
        except requests.ConnectionError as e:
            logger.error(f'BCRA UVA API connection error: {e}')
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
        cached_data = self._get_cached_data('uva_rate_history')
        if cached_data is not None:
            return cached_data

        try:
            one_year_ago = (date.today() - timedelta(days=365)).isoformat()
            response = requests.get(
                f'https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/{self.UVA_RATE_ID}',
                params={'desde': one_year_ago},
                headers=self.HEADERS,
                timeout=self.REQUEST_TIMEOUT
            )

            if response.status_code == 429:
                logger.warning('BCRA UVA rate limit exceeded')
                return None

            if response.status_code == 200:
                data = response.json()
                history = data.get('results', [{}])[0].get('detalle', [])
                self._set_cached_data('uva_rate_history', history)
                return history

            logger.warning(f'BCRA UVA rate API status: {response.status_code}')

        except requests.Timeout:
            logger.error('BCRA UVA rate API request timed out')
        except requests.ConnectionError as e:
            logger.error(f'BCRA UVA rate API connection error: {e}')
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
                headers=self.HEADERS,
                timeout=self.REQUEST_TIMEOUT
            )

            if response.status_code == 429:
                logger.warning('CoinGecko historical rate limit exceeded')
                return None

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

            logger.warning(f'CoinGecko historical API status: {response.status_code}')

        except requests.Timeout:
            logger.error('CoinGecko historical API request timed out')
        except requests.ConnectionError as e:
            logger.error(f'CoinGecko historical API connection error: {e}')
        except Exception as e:
            logger.error(f'CoinGecko historical API error: {e}')

        return None

    def _find_closest_date(
        self,
        data: list[dict],
        target_date: date,
        prefer_before: bool = True
    ) -> Optional[dict]:
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