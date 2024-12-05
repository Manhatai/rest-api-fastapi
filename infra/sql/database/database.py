from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

__DB_BASE_HOST = f"{os.getenv('REST_API_DB_HOST')}:{os.getenv('REST_API_DB_PORT')}"
__DB_CREDENTIALS = f"{os.getenv('REST_API_DB_LOGIN')}:{os.getenv('REST_API_DB_PASSWORD')}"
SQLALCHEMY_DATABASE_URI = f'postgresql://{__DB_CREDENTIALS}@{__DB_BASE_HOST}/{os.getenv("REST_API_DB_NAME")}'

engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()