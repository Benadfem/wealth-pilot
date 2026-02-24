# We're going to build a simple API with ONE endpoint that responds with a message. '
# 'That's it. Nothing fancy. Just the absolute basics. 

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()



# in-memory database 
# In-memory database with seeded data
transactions_db = [
    {"id": 1, "amount": 5000.00, "description": "Lunch at KFC", "date": "2026-02-24", "category": "food"},
    {"id": 2, "amount": 15000.00, "description": "Uber ride to Island", "date": "2026-02-24", "category": "transport"},
    {"id": 3, "amount": 250000.00, "description": "February salary", "date": "2026-02-24", "category": "income"},
]
transaction_counter = 4  # starts at 4 since 1,2,3 already exist

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
def get_transactions():
    return {"transactions": transactions_db}


# a request for transaction individual transaction
# pydantic see it as dynamic variables.by {}
# return specific / one transaction 
@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: int):
    return {"transaction_id" : transaction_id}

# a method to add transaction data
@app.post("/transactions")
def create_transaction(transaction: Transaction):
    global transaction_counter
    new_transaction ={
        "id": transaction_counter,
        "amount": transaction.amount,
        "description" : transaction.description,
        "date": transaction.date,
        "category": transaction.category
    }
    #update the transaction_db list 
    transactions_db.append(new_transaction)
    transaction_counter += 1

    return new_transaction 