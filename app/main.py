# We're going to build a simple API with ONE endpoint that responds with a message. '
# 'That's it. Nothing fancy. Just the absolute basics. 

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session # type: ignore
from app.database import SessionLocal, engine
from app import models


models.Base.metadata.create_all(bind=engine)
app = FastAPI()



# DEPENDENCY: Database Session 
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

# let us create model for the transaction that inherits form the BaseModel 
class Transaction(BaseModel):
    amount: float
    description: str
    date: str
    category: str


# to get request from the server, use the decorator as below 
@app.get("/")
# declare the function to perform the get request 
def read_root():
    return {"message": "Hello from Wealth-pilot"}

@app.get("/health")
def read_health():
    return {"status": "healthy",
            "service":"wealth-pilot"
            }

# returns all transactions 
@app.get("/transactions")
def get_transactions(db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).all()
    return {"transactions": transactions}


# a request for transaction individual transaction
# pydantic see it as dynamic variables.by {}
# return specific / one transaction 
@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id).first()
    return transaction

# a method to add transaction data
@app.post("/transactions")
def create_transaction(transaction: Transaction, db: Session = Depends(get_db)):
    db_transaction = models.Transaction(
        amount=transaction.amount,
        description=transaction.description,
        date=transaction.date,
        category=transaction.category
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction