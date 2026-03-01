from sqlalchemy import Column, Integer, Float , String # pyright: ignore[reportMissingImports]
from database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    description = Column(String)
    date = Column(String)
    category = Column(String)