from sqlalchemy  import create_engine # type: ignore
from sqlalchemy.orm import declarative_base # type: ignore
from sqlalchemy.orm  import sessionmaker # type: ignore

DATABASE_URL = "postgresql://postgres:Benadfem@01@localhost/wealth_pilot" 

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()