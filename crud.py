from sqlalchemy.orm import Session

import models, schemas
import random


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_sentiment_by_subreddit_and_topic(db: Session, subreddit: str, topic: str):
    return db.query(models.Sentiment).filter(models.Sentiment.subreddit == subreddit, models.Sentiment.topic == topic).first()

def createSentiment(db: Session, sentiment: schemas.SentimentCreate):
        db_sentiment = models.Sentiment(subreddit=sentiment.subreddit, topic=sentiment.topic,sentimentrating=sentiment.sentimentrating)
        db.add(db_sentiment)
        db.commit()
        db.refresh(db_sentiment)
        return db_sentiment