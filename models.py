# models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Signal(Base):
    __tablename__ = 'signals'
    
    id = Column(Integer, primary_key=True)
    currency_pair = Column(String)
    timeframe = Column(String)
    strategy = Column(String)
    signal = Column(String)
    confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# SQLite DB auto-create
engine = create_engine('sqlite:///signals.db', echo=False)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
