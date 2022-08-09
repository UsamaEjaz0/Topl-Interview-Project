from abc import ABC, abstractmethod
from typing import Union

from expression import pipe
from expression.collections import Map, Seq, seq
from pydantic import BaseModel


class MetadataStrategy(ABC):
    """
    Abstract class to specify a metadata strategy
    """
    @abstractmethod
    def generate(self, article: 'Article') -> Map[str, any]:
        """
        Generates metadata from the article
        :param article: Article object
        :return: A map containing character_count, word_count, line_count, unique_word_count and most
        _frequent_word_count in the article
        """
        ...


def map_merge(map1: Map[str, any], map2: Map[str, any]) -> Map[str, any]:
    """
    Merges two maps
    :param map1: 1st Map to merge
    :param map2: 2nd Map to merge
    :return: A unionised map of map1 and map2
    """
    return Map.of_seq((*map1.items(), *map2.items()))


class KeywordFrequencyMetadata(MetadataStrategy):
    """
    A metadata class to generate keyword frequency map
    """
    def generate(self, article: 'Article') -> Map[str, any]:
        return Map.of_seq((
            ("character_count", len([*article.content])),
            ("word_count", len(article.content.split(" "))),
            ("line_count", len(article.content.split(".")) + 1),
            ("unique_word_count", len(set(article.content.split(" ")))),
            ("most_frequent_words", list(
                pipe(
                    sorted(
                        Seq.of_iterable(set(article.content.split(" "))).map(lambda w: (w, article.content.count(w))),
                        key=lambda x: x[1],
                        reverse=True
                    ),
                    seq.take(10),
                    seq.map(lambda i: Map.of_seq((
                        ("word", i[0]),
                        ("count", i[1])
                    )))
                )
            )),
        ))


class Article(BaseModel):
    """
    Article model class
    """
    name: str
    author: str
    description: str
    content: str

    __strategies: Seq[MetadataStrategy] = Seq.of(KeywordFrequencyMetadata())

    def dict(
            self,
            *,
            include: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
            exclude: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
            by_alias: bool = False,
            skip_defaults: bool = None,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
    ) -> 'DictStrAny':

        return {
            **super().dict(
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                skip_defaults=skip_defaults,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
            ),
            "metadata": self.metadata,
        }

    @property
    def metadata(self) -> Map[str, any]:
        """
        Creates a Map of metadata
        :return: a Map containing metadata of the article
        """
        return self.__strategies \
            .map(lambda strategy: strategy.generate(self)) \
            .fold(map_merge, Map.empty())
