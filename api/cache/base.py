from typing import TypeVar, Generic

from expression import Try, effect
from expression.collections import Seq

from api.cache.strategy.base import CacheStrategy
from api.cache.strategy.memory import MemoryStrategy
from api.models.article import Article
from api.models.author import Author
from api.sources.base import NewsSource

_T = TypeVar('_T', bound=NewsSource)


class CachedNewsSource(NewsSource, Generic[_T]):
    """
    Cached New Source class
    """
    __internal: _T
    __strategy: CacheStrategy

    def __init__(self, source: _T, strategy: CacheStrategy = MemoryStrategy()) -> None:
        super().__init__()
        self.__internal = source
        self.__strategy = strategy

    @classmethod
    def name(cls) -> str:
        return 'CachedNewsSource'

    @effect.try_[Seq[Article]]()
    def fetch(self, count: int = 10, offset: int = 0) -> Try[Seq[Article]]:
        key = CacheStrategy.CachedFetch(count, offset)
        if key not in self.__strategy:
            self.__strategy[key] = yield from self.__internal.fetch(count, offset)

        return self.__strategy[key]

    @effect.try_[Seq[Article]]()
    def search(self, item: Author | Seq[str]) -> Try[Seq[Article]]:
        key = CacheStrategy.CachedSearch(item) \
            if isinstance(item, Author) \
            else CacheStrategy.CachedSearch(tuple(item))

        if key not in self.__strategy:
            self.__strategy[key] = yield from self.__internal.search(item)

        return self.__strategy[key]
