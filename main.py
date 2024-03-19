from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.orm import Session
from models import QuoteModel, engine
from schema import Quote 

app = FastAPI()


Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
	db = SessionLocal()
	try:
		yield db 
	finally:
		db.close()

@app.post ("/quotes", response_model=Quote)
def create_quote(content: str, db: Session = Depends(get_db)):
	new_quote = Quote(content=content)
	db.add(new_quote)
	db.commit()
	db.refresh(new_quote)
	return new_quote

@app.get("/quotes/random/", response_model=Quote)
def get_random_quote (db: Session = Depends(get_db)):
	quote = db.query(Quote).order_by(func.random()).first()
	if quote is None:
		raise HTTPException(status_code=404, detail="Quote not found")
	return quote

