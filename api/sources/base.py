from abc import ABC, abstractmethod

from api.models.author import Author
from api.models.article import Article


class NewsSource(ABC):
    @classmethod
    @abstractmethod
    def name(cls) -> str: ...

    @abstractmethod
    def fetch(self, count: int = 10, offset: int = 0) -> list[Article]: ...

    @abstractmethod
    def search(self, item: Author | list[str]) -> list[Article]: ...
