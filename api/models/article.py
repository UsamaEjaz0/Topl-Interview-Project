from pydantic import BaseModel


class Article(BaseModel):
    name: str
    author: str
    description: str
    content: str
