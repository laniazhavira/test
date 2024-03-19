from pydantic import BaseModel 

class Quote(BaseModel):
	id: int
	content: str

	class Config:
		orm_mode = True
