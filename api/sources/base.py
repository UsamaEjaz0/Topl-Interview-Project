from abc import ABC, abstractmethod

from expression import Try
from expression.collections import Seq

from api.models.article import Article
from api.models.author import Author


class NewsSource(ABC):
    @classmethod
    @abstractmethod
    def name(cls) -> str: ...

    @abstractmethod
    def fetch(self, count: int = 10, offset: int = 0) -> Try[Seq[Article]]: ...

    @abstractmethod
    def search(self, item: Author | Seq[str]) -> Try[Seq[Article]]: ...
