import asyncio, json, redis
from pymongo import MongoClient, ASCENDING
from fastapi import FastAPI
from config import REDIS_HOST, REDIS_PORT, REDIS_CHANNEL, MONGO_URL, MONGO_DB, MONGO_COL

app = FastAPI(title="news-processor")


def col():
    c = MongoClient(MONGO_URL)
    collection = c[MONGO_DB][MONGO_COL]
    collection.create_index([("url", ASCENDING)], unique=True)
    return collection


async def process_messages(collection):
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    p = r.pubsub()
    p.subscribe(REDIS_CHANNEL)
    for msg in p.listen():
        if msg.get("type") != "message":
            await asyncio.sleep(0)
            continue
        try:
            article = json.loads(msg["data"])
            url = article.get("url")
            if url and url.startswith("http"):
                collection.update_one(
                    {"url": url},
                    {"$set": {
                        "url": url,
                        "title": article.get("title"),
                        "summary": article.get("summary")
                    }},
                    upsert=True
                )
        except (json.JSONDecodeError, KeyError, AttributeError):
            pass
        await asyncio.sleep(0)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
async def run_startup():
    collection = col()
    asyncio.create_task(process_messages(collection))
