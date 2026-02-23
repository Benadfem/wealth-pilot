# We're going to build a simple API with ONE endpoint that responds with a message. '
# 'That's it. Nothing fancy. Just the absolute basics. 

from fastapi import FastAPI

app = FastAPI()

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

# a request for transaction
@app.get("/transactions")
def get_transactions():
    return {"transactions" : []}

# a method to add transaction data
@app.post("/transactions")
def create_transaction():
    return {"Message": "Transaction created sucessfully"}