import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

# Assume a default db exists (usually 'postgres' exists by default)
# So it doesn't fail if 'imaginairy' db isn't created yet, let's use 'postgres' db for now.
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./imaginairy.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Generation(Base):
    __tablename__ = "generations"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String, index=True)
    model_name = Column(String)
    image_path = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Warning: Could not connect to PostgreSQL or create tables. {e}")
