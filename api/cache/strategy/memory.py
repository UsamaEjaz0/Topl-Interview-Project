from typing import Optional

from api.cache.strategy.base import CacheStrategy
from api.models.article import Article


class MemoryStrategy(CacheStrategy):
    """
    A memory caching strategy class
    """
    __cache: dict[CacheStrategy.CachedFetch | CacheStrategy.CachedSearch, list[Article]] = {}

    def _set(self, data: CacheStrategy.CachedFetch | CacheStrategy.CachedSearch, result: list[Article]) -> None:
        self.__cache[data] = result

    def _get(self, data: CacheStrategy.CachedFetch | CacheStrategy.CachedSearch) -> Optional[list[Article]]:
        return self.__cache.get(data, None)
