from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
import os
from models import Base

load_dotenv()


# DATABASE_URL = os.getenv('sqlite:///./identifier.sqlite')


# engine = create_engine(
#     DATABASE_URL,
#     echo=False,
#     connect_args={'check_same_thread': False} if 'sqlite' in DATABASE_URL else {},
#
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# db_session = scoped_session(SessionLocal)

def get_engine():
    """create and return database engine  """
    db_path_url = os.getenv('db_path_url', 'sqlite:///./identifier.sqlite')

    db_path = os.path.dirname(db_path_url)
    if db_path_url and not os.path.exists(db_path):
        os.makedirs(db_path)

    engine = create_engine(db_path_url, connect_args={'check_same_thread': False}, echo=False)

    return engine


def init_db():
    """initialize database - create all tables"""

    engine = get_engine()
    Base.metadata.create_all(engine)
    return engine




def get_db_session():

    """get db session"""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()



