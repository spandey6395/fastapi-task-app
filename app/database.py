from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")
logger.debug(f"Database URL: {DATABASE_URL}")
engine = create_engine(DATABASE_URL, echo=True)  # Logs SQL commands
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        logger.debug("Testing database connection")
        with db.begin():
            db.execute(text("SELECT 1"))
        logger.debug("Connection test successful, yielding session")
        yield db
    except Exception as e:
        logger.error(f"Database session error: {type(e).__name__} - {str(e)}")
        raise
    finally:
        logger.debug("Closing database session")
        db.close()
