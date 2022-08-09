from fastapi import FastAPI

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


@app.get("/")
def fetch(query: int = 10, source: str = "default") -> list[Article]:
    return sources[source].fetch(query)


@app.get("/search")
def search(query: str, source: str = "default") -> list[Article]:
    return sources[source].search(query.split(" "))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
