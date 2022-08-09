import unittest

from expression import Try, Success
from expression.collections import Seq

from api.cache.base import CachedNewsSource
from api.models.article import Article
from api.models.author import Author
from api.sources.base import NewsSource


class CacheTest(unittest.TestCase):
    class _MockNewsSource(NewsSource):
        fetch_count: int = 0
        search_count: int = 0

        @classmethod
        def name(cls) -> str:
            return "Cache"

        def fetch(self, count: int = 10, offset: int = 0) -> Try[Seq[Article]]:
            self.fetch_count += 1
            return Success(Seq.of(Article(
                name="Article",
                author="Test",
                content="Test",
                description="Test"
            )))

        def search(self, item: Author | Seq[str]) -> Try[Seq[Article]]:
            self.search_count += 1
            return Success(Seq.of(Article(
                name="Article",
                author="Test",
                content="Test",
                description="Test"
            )))

    def setUp(self) -> None:
        super().setUp()
        self.internal = CacheTest._MockNewsSource()
        self.instance = CachedNewsSource(self.internal)

    def test_fetch(self):
        for i in range(10):
            self.instance.fetch()

        assert self.internal.fetch_count == 1

    def test_search(self):
        keywords = Seq.of("Test", "Keywords")
        for i in range(10):
            self.instance.search(keywords)

        assert self.internal.search_count == 1
        keywords = Seq.of("Test", "Keywords", "New")
        for i in range(10):
            self.instance.search(keywords)

        assert self.internal.search_count == 2
