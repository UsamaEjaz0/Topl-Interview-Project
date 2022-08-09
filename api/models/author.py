from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Author:
    author: str
