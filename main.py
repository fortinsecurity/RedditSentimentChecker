from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class SentimentRequest(BaseModel):
    subreddit: str
    topic: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

'''
query params example
'''

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

'''
GET /sentiment?subreddit=crypto&topic=etherium
'''

fake_sentiment_db = [{
    "subreddit":"crypto",
    "topic":"etherium",
    "sentiment":"8"
    }]

@app.get("/sentiment/")
def getSentiment(subreddit: str, topic: str):
    return fake_sentiment_db[0]

# to run: uvicorn main:app --reload