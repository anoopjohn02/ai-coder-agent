"""
SQL Engine module
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.config import Db as db

engine = create_engine(db.connUrl, echo=False)
Session = sessionmaker(bind=engine)


def check_db():
    """
    Method to check db connection
    """
    with engine.connect() as conn:
        stmt = text("select * from pg_database")
        print(conn.execute(stmt).fetchall())
