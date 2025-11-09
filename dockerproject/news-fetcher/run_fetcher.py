import time, json, requests, threading
import redis
from fastapi import FastAPI
from config import (
    REDIS_HOST, REDIS_PORT, REDIS_CHANNEL,
    NEWSAPI_KEY, NEWSAPI_COUNTRY, NEWSAPI_PAGE_SIZE, NEWSAPI_INTERVAL_SEC, NEWSAPI_URL
)

URL = NEWSAPI_URL
svc = FastAPI(title="news-fetcher")
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def lookoverarticals():
    params = {
        "apiKey": NEWSAPI_KEY,
        "category": "technology",
        "pageSize": NEWSAPI_PAGE_SIZE,
    }
    resp = requests.get(URL, params=params)
    data = resp.json()
    out = []
    for a in data["articles"]:
        url = (a.get("url") or "").strip()
        title = (a.get("title") or "").strip()
        summary = (a.get("description") or "").strip()
        if url.startswith("http") and title:
            out.append({"url": url, "title": title, "summary": summary})
    return out


def publish(arts):
    for a in arts:
        r.publish(REDIS_CHANNEL, json.dumps(a))


@svc.get("/health")
def health():
    return {"status": "ok"}


@svc.on_event("startup")
def start():
    def loop():
        while True:
            arts = lookoverarticals()
            publish(arts)
            time.sleep(NEWSAPI_INTERVAL_SEC)

    threading.Thread(target=loop, daemon=True).start()
