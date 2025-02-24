from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Email(Base):
    __tablename__ = 'emails'
    
    id = Column(Integer, primary_key=True)
    message_id = Column(String, unique=True)
    subject = Column(String)
    sender = Column(String)
    received_at = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)
    response_sent = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<Email {self.subject}>"

class Token(Base):
    """Token model for storing OAuth tokens."""
    
    __tablename__ = 'tokens'
    
    id = Column(String, primary_key=True)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String)
    expires_at = Column(DateTime, nullable=False) 