from typing import cast, Callable

from expression import Failure, Ok, Try
from expression.collections import seq, Seq
from fastapi import FastAPI, HTTPException

from api.cache.base import CachedNewsSource
from api.models.article import Article
from api.sources.base import NewsSource
from api.sources.gnews import GNewsSource

__gnews = CachedNewsSource(GNewsSource())
sources: dict[str, NewsSource] = {
    'default': __gnews,
    'gnews': __gnews,
}

app = FastAPI()


def execute_request(source: str, action: Callable[[], Try[Seq[Article]]]) -> list[Article]:
    """
    Executes a request based
    :param source: A news source
    :param action: A callable object
    :return: list of articles fetched from the news source by the callable action
    """
    if source not in sources:
        raise HTTPException(status_code=404, detail=f"Source {source} not found")

    res = action()
    if res.is_ok():
        return list(cast(Ok, res).value)
    else:
        raise HTTPException(status_code=400, detail=cast(Failure, res).message)


@app.get("/", description="Fetch N number of articles")
def fetch(count: int = 10, source: str = "default") -> list[Article]:
    return execute_request(source, lambda: sources[source].fetch(count))


@app.get("/search", description="Query articles by list of keywords or author name")
def search(query: str, source: str = "default") -> list[Article]:
    return execute_request(source, lambda: sources[source].search(seq.of_iterable(query.split(" "))))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
