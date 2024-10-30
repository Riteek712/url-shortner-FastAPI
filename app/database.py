from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL
from app.models import Base 

# Initialize the engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the database (only if they don't already exist)
# Need to add migration methods.
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print("Error creating tables:", e)
