from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
from config import MONGO_URL, MONGO_DB, MONGO_COL
from html_builder import HTMLBuilder

svc = FastAPI(title="news-frontend")


def collection():
    return MongoClient(MONGO_URL)[MONGO_DB][MONGO_COL]


@svc.get("/health")
def health():
    return {"status": "ok"}


@svc.get("/articles", response_class=HTMLResponse)
def list_urls():
    docs = collection().find({}, {"_id": 0, "url": 1}).sort([("_id", -1)])
    urls = [d["url"] for d in docs if d.get("url") and d["url"].startswith("http")]
    return HTMLBuilder.build_page("News Links", urls)
