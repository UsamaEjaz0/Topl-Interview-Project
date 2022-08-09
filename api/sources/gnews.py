from __future__ import annotations

import requests
from pydantic import BaseModel
from requests import Response

from api.models.article import Article
from api.models.author import Author
from api.sources.base import NewsSource


class GNewsSourceInfo(BaseModel):
    name: str
    url: str


class GNewsArticle(BaseModel):
    title: str
    description: str
    content: str
    url: str
    image: str
    publishedAt: str
    source: GNewsSourceInfo

    def map_to_article(self) -> Article:
        return Article(
            name=self.title,
            author=self.source.name,
            description=self.description,
            content=self.content,
        )


class GNewSourceArticles(BaseModel):
    totalArticles: int
    articles: list[GNewsArticle]


class GNewsSource(NewsSource):
    # Move to more secure location like .env
    __token: str = "fb59814ed56f1a263277c40b0a1ea6a8"

    def __get(self, endpoint: str, **kwargs) -> Response:
        return requests.get(f"https://gnews.io/api/v4/{endpoint}", params={"token": self.__token, **kwargs})

    @classmethod
    def name(cls) -> str: return 'Google News'

    def fetch(self, count: int = 10, offset: int = 0) -> list[Article]:
        articles = GNewSourceArticles.parse_obj(self.__get("top-headlines").json())
        return [
            article.map_to_article() for article in articles.articles
        ]

    def search(self, item: Author | list[str]) -> list[Article]:
        if isinstance(item, Author):
            raise NotImplementedError("Search by author is not supported by this source")

        tokens = [f'"{token}"' for token in item]
        articles = GNewSourceArticles.parse_obj(self.__get("search", q=" ".join(tokens)).json())
        return [
            article.map_to_article() for article in articles.articles
        ]
