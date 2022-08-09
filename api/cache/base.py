from typing import TypeVar, Generic

from api.cache.strategy.base import CacheStrategy
from api.cache.strategy.memory import MemoryStrategy
from api.models.article import Article
from api.models.author import Author
from api.sources.base import NewsSource

_T = TypeVar('_T', bound=NewsSource)


class CachedNewsSource(NewsSource, Generic[_T]):
    __internal: _T
    __strategy: CacheStrategy

    def __init__(self, source: _T, strategy: CacheStrategy = MemoryStrategy()) -> None:
        super().__init__()
        self.__internal = source
        self.__strategy = strategy

    @classmethod
    def name(cls) -> str:
        return 'CachedNewsSource'

    def fetch(self, count: int = 10, offset: int = 0) -> list[Article]:
        key = CacheStrategy.CachedFetch(count, offset)
        if key not in self.__strategy:
            self.__strategy[key] = self.__internal.fetch(count, offset)

        return self.__strategy[key]

    def search(self, item: Author | list[str]) -> list[Article]:
        key = CacheStrategy.CachedSearch(item) \
            if isinstance(item, Author) \
            else CacheStrategy.CachedSearch(tuple(item))

        if key not in self.__strategy:
            self.__strategy[key] = self.__internal.search(item)

        return self.__strategy[key]
