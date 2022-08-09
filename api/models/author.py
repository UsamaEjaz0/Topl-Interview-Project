from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Author:
    """
    Author model class
    """
    author: str
