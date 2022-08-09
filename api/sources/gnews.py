from __future__ import annotations

import requests
from expression import Try, effect, pipe, Success, Failure
from expression.collections import Seq, seq
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
    __token: str = "b2afdfba15da9f459a32cbee57cca1da"

    def __get(self, endpoint: str, **kwargs) -> Try[Response]:
        try:
            response = requests.get(f"https://gnews.io/api/v4/{endpoint}", params={"token": self.__token, **kwargs})
            if response.status_code != 200:
                return Failure(ValueError(f"{response.status_code}: {response.text}"))

            return Success(response)
        except Exception as e:
            return Failure(e)

    @staticmethod
    def __parse(json: dict) -> Try[GNewSourceArticles]:
        try:
            return Success(GNewSourceArticles.parse_obj(json))
        except Exception as e:
            return Failure(e)

    @classmethod
    def name(cls) -> str:
        return 'Google News'

    @effect.try_[Seq[Article]]()
    def fetch(self, count: int = 10, offset: int = 0) -> Try[Seq[Article]]:
        res: Response = yield from self.__get("top-headlines", max=count)
        articles: GNewSourceArticles = yield from self.__parse(res.json())
        return pipe(
            articles.articles,
            seq.map(lambda x: x.map_to_article())
        )

    @effect.try_[Seq[Article]]()
    def search(self, item: Author | Seq[str]) -> Try[Seq[Article]]:
        if isinstance(item, Author):
            return Failure(NotImplementedError("Search by author is not supported by this source"))

        tokens = pipe(
            item,
            seq.map(lambda i: f'"{i}"'),
            seq.fold(lambda acc, i: f"{acc} {i}".strip(), "")
        )

        res: Response = yield from self.__get("search", q=tokens)
        gnews_articles: GNewSourceArticles = yield from self.__parse(res.json())
        return pipe(
            gnews_articles.articles,
            seq.map(lambda x: x.map_to_article())
        )

