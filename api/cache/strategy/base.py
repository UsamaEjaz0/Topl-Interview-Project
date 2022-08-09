from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from api.models.article import Article
from api.models.author import Author


class CacheStrategy(ABC):
    @dataclass(frozen=True, eq=True)
    class CachedFetch:
        count: int
        offset: int

    @dataclass(frozen=True, eq=True)
    class CachedSearch:
        item: Author | tuple[str]

    def __setitem__(self, key: CachedFetch | CachedSearch, value: list[Article]) -> None:
        self._set(key, value)

    def __getitem__(self, item: CachedFetch | CachedSearch) -> list[Article]:
        return self._get(item)

    def __contains__(self, item: CachedFetch | CachedSearch) -> bool:
        return self._get(item) is not None

    @abstractmethod
    def _set(self, data: CachedFetch | CachedSearch, result: list[Article]) -> None: ...

    @abstractmethod
    def _get(self, data: CachedFetch | CachedSearch) -> Optional[list[Article]]: ...
