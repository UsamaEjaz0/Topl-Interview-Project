from fastapi import FastAPI

from api.models.article import Article
from api.sources.base import NewsSource
from api.sources.gnews import GNewsSource

sources: dict[str, NewsSource] = {
    'default': GNewsSource(),
    'gnews': GNewsSource(),
}

app = FastAPI()


@app.get("/")
def fetch(query: int = 10, source: str = "default") -> list[Article]:
    return sources[source].fetch(query)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
