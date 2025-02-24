from database import SessionLocal, Email
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL


def sauvegarder_email(
    sender, subject, content, agent_id, decision_ia="", response_sent=""
):
    session = SessionLocal()
    new_email = Email(
        sender=sender,
        subject=subject,
        content=content,
        decision_ia=decision_ia,
        response_sent=response_sent,
        agent_id=agent_id,
    )
    try:
        session.add(new_email)
        session.commit()
    except IntegrityError:
        session.rollback()
        # Gérer les cas d'erreur
    finally:
        session.close()

def init_db():
    """Initialise la connexion à la base de données"""
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return SessionLocal()
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la base de données : {e}")
        return None
