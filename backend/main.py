'''
learning the stack:
FastAPI
SQLAlchemy
pydantic
regex
TextBlob (NLP)
react.js

'''

import datetime
from typing import Union
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from createSentimentLogic import getSentimentFinal
from createSentimentLogic import queryToDatabase, totalSentimentForTopicAndSubreddit

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


# #GET /sentiment?subreddit=crypto&topic=etherium
# @app.get("/sentiment/", response_model=schemas.Sentiment)
# def read_Sentiment(subreddit: str, topic: str, db: Session = Depends(get_db)):
#     sentiment = crud.get_sentiment_by_subreddit_and_topic(db, subreddit=subreddit, topic=topic)
#     return sentiment

#GET /sentiment?subreddit=crypto&topic=etherium

""" 
GET sentiment will call sentiment logic's getSentimentFinal, return the result, and store the comments using and then crud.create_sentiment 
"""
@app.get("/sentiment/")
def read_Sentiment(subreddit: str = Query(regex="^\w*$"), topic: str = Query(regex="^\w*$"), limit: Union[int, None] = 25, db: Session = Depends(get_db)):
    print(topic)
    comments = queryToDatabase(subreddit,topic,limit)
    for comment in comments:
        now = datetime.datetime.now()
        commentDict = {
            "subreddit":comment[0],
            "topic":comment[1],
            "body":comment[2],
            "sentiment":comment[3],
            "timestamp": now
        }
        print("commentDict before curding to DB: ", commentDict)
        try:
            crud.create_sentiment(db=db, sentiment=commentDict)
        except Exception as e:
            print(e)
    res = totalSentimentForTopicAndSubreddit(comments)
    

    # return {"subreddit":"pokemon","topic":"pikachu","sentiment":0.07857142857142858}
    return {"subreddit":subreddit, "topic":topic, "sentiment":res}
    
@app.post("/sentiment/", response_model=schemas.Sentiment)
def create_Sentiment(sentiment:schemas.SentimentCreate, db: Session = Depends(get_db)):
    db_sentiment = crud.get_sentiment_by_subreddit_and_topic(db, subreddit=sentiment.subreddit, topic=sentiment.topic)
    if db_sentiment:
        raise HTTPException(status_code=400, detail="Sentiment already exists")
    return crud.createSentiment(db=db, sentiment=sentiment)

# to run: uvicorn main:app --reload