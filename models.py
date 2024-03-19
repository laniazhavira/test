from sqlalchemy import Column, Integer, String ,create_engine
from sqlalchemy.ext.declarative import declarative_base 
from schema import quote

Base = declarative_base()

class Quote(Base):
	__tablename__ = 'quotes'

	id = Column(Integer, primary_key=True, index=True)
	content = Column(String, nullable=False)

def ro_dict(self):
	return{"id": self.id, "content": self.content}
