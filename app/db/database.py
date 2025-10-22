from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
import os
from app.db.models import Base

load_dotenv()

db_path_url = os.getenv('DATABASE_URL', 'sqlite:///./identifier.sqlite')

if db_path_url.startswith('sqlite://'):
    file_path = db_path_url.replace('sqlite://', '')
    db_dir = os.path.dirname(file_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

engine = create_engine(
    db_path_url,
    connect_args={"check_same_thread": False},
    echo=False)

# def get_engine():
#     """create and return database engine  """
#
#     db_path = os.path.dirname(db_path_url)
#     if db_path_url and not os.path.exists(db_path):
#         os.makedirs(db_path)
#
#     engine = create_engine(db_path_url, connect_args={'check_same_thread': False}, echo=False)
#
#     return engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """initialize database - create all tables"""
    Base.metadata.create_all(engine)
    print("Database created successfully!")


def get_db_session():
    """get db session"""
    return SessionLocal()
