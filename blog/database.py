from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

database_url = "sqlite:///./blog.db"
engine = create_engine(database_url, connect_args = {"check_same_thread": False})

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)