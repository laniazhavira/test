from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from models import Base, Quote
from schema import Quote as QuoteModel
from database import get_all_quotes
from typing import List
import random

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./quotes.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
        db = SessionLocal()
        try:
                yield db
        finally:
                db.close()
@app.get("/")
def read_root():
        return {"message": "Go to /quotes/random/ to get your quotes of the day"}

@app.post ("/quotes", response_model=QuoteModel)
def create_quote(content: str, db: Session = Depends(get_db)):
        new_quote = Quote(content=content)
        db.add(new_quote)
        db.commit()
        db.refresh(new_quote)
        return new_quote

@app.get("/quotes/random/", response_model=QuoteModel)
def get_random_quote (db: Session = Depends(get_db)):
        quote = db.query(Quote).order_by(func.random()).first()
        if quote is None:
                raise HTTPException(status_code=404, detail="Quote not found")
        return quote
