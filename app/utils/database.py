from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ..config.settings import Config
from datetime import datetime, timedelta
from ..models import Token

DATABASE_URL = Config.DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    """Initialise la connexion à la base de données"""
    try:
        engine = create_engine(Config.DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return SessionLocal()
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la base de données : {e}")
        return None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_token(token_data):
    """Save token to database."""
    session = SessionLocal()
    try:
        # Calculer la date d'expiration
        expires_at = datetime.now() + timedelta(seconds=token_data['expires_in'])
        
        # Créer ou mettre à jour le token
        token = session.query(Token).first()
        if not token:
            token = Token()
            
        token.access_token = token_data['access_token']
        token.refresh_token = token_data.get('refresh_token')
        token.expires_at = expires_at
        
        session.add(token)
        session.commit()
        return token
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_token():
    """Get the current token from database."""
    session = SessionLocal()
    try:
        return session.query(Token).first()
    finally:
        session.close() 