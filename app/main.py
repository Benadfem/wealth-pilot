# We're going to build a simple API with ONE endpoint that responds with a message. '
# 'That's it. Nothing fancy. Just the absolute basics. 


from pydantic import BaseModel
from sqlalchemy.orm import Session # type: ignore
from app.database import SessionLocal, engine
from app import models

# import the modules from the project
from app import auth
from app.schemas import UserCreate, Token, UserLogin
from app.models import User

# this import the security for the transactions endpoint 
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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



# a request for transaction individual transaction
# pydantic see it as dynamic variables.by {}
# return specific / one transaction 
@app.get("/transactions")
def get_transactions(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = auth.verify_token(token, db)
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authorized")
    transactions = db.query(models.Transaction).all()
    return {"transactions": transactions}

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


# Register endpoint
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if user.password != user.confirm_password:
        return {"error": "Passwords do not match"}
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        return {"error": "Username already taken"}
    hashed = auth.hash_password(user.password)
    new_user = User(username=user.username, password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Account created successfully"}

# Login endpoint
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == form_data.username).first()
    if not db_user:
        return {"error": "Invalid username or password"}
    if not auth.verify_password(form_data.password, db_user.password):
        return {"error": "Invalid username or password"}
    token = auth.create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}